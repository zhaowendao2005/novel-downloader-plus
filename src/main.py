from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from PyQt5.QtGui import QColor,QPixmap, QPainter
from picture_manager import BackgroundSetter
from src.windows2 import Ui_MainWindow
import novel_downloader_2
from PyQt5.QtGui import QMouseEvent
import os
import threading
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    log_signal = QtCore.pyqtSignal(str)  # 新增日志信号
    # 定义线程信号
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(str)
    result = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setupUi(self)  # Setup the UI from the imported class
        download_thread = threading.Thread(target=self.download_novel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #创建线程初始对象
        self.download_thread = None  # 线程控制器
        self.worker = None  # 工作对象


        #日志输出

            # 配置日志系统
        self.log_signal.connect(self.update_console)
        qt_handler = QtLogHandler(self.log_signal)
        qt_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logging.getLogger().addHandler(qt_handler)  # 动态挂载处理器


        #构件pushButton自定义
        self.toolButton_exitWindow.setIcon(Icon(FluentIcon.CLOSE))
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))
        self.toolButton_removeWindow.setIcon(Icon(FluentIcon.MINIMIZE))
        self.toolButton_maximiseWindow.setIcon(Icon(FluentIcon.ZOOM))




        #图片构件自定义
        background_setter = BackgroundSetter(self.widget_toolbox_page1, "../QT/resource/tool_box_page1_background.png", 0.8)
        background_setter = BackgroundSetter(self.label, "../QT/resource/label_2.png", 0.3)
        background_setter = BackgroundSetter(self.frame_MainBackground, "../QT/resource/image.png", 0.9)
        background_setter = BackgroundSetter(self.frame_7, "../QT/resource/frame_7.png", 0.4)
        background_setter = BackgroundSetter(self.frame_9, "../QT/resource/frame_9.png", 0.4)
        self.pushButton_downloader.clicked.connect(self.download_novel)
        self.toolButton_exitWindow.clicked.connect(self.close)
        self.toolButton_removeWindow.clicked.connect(self.showMinimized)
        self.toolButton_maximiseWindow.clicked.connect(self.showMaximized)
        #日志输出函数
    def update_console(self, message):
        self.plainTextEdit_console.appendPlainText(message)





    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.isInResizeZone(event.pos()):  # 判断是否在右下角调整区域
                self.resizing = True
                self.resizeStart = event.pos()
                self.resizeSize = self.size()
            else:  # 如果不在调整区域，则记录鼠标偏移量用于窗口移动
                self.resizing = False
                self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if event.buttons() & Qt.LeftButton:  # 按住鼠标左键时
            if self.resizing:  # 如果正在调整大小
                delta = event.pos() - self.resizeStart
                self.resize(self.resizeSize.width() + delta.x(),
                            self.resizeSize.height() + delta.y())
            else:  # 如果没有在调整大小区域，则移动窗口
                self.move(event.globalPos() - self.offset)
        else:  # 鼠标未按下时，仅改变光标
            if self.isInResizeZone(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)  # 右下角调整大小光标
            else:
                self.setCursor(Qt.ArrowCursor)  # 默认箭头光标

    def isInResizeZone(self, pos):
        # 判断鼠标是否位于窗口右下角 10 像素范围内
        return (pos.x() >= self.width() - 30 and pos.y() >= self.height() - 30)

    def download_novel(self):
        """重构后的下载方法"""
        if self.download_thread and self.download_thread.isRunning():
            self.update_console("下载正在进行中...")
            return

        # 组装参数
        params = {
            "baseurl": self.line_edit_baseurl.text(),
            "url_path": self.lineEdit_urlpath.text(),
            "selector_content": self.lineEdit_contentSelector.text(),
            "selector_chapter": self.lineEdit_chapterListSelector.text(),
            "output_file": self._generate_output_filename(),
            "max_workers": self._get_worker_count()
        }

        # 创建线程对象
        self.download_thread = QtCore.QThread()
        self.worker = DownloadWorker(params)
        self.worker.moveToThread(self.download_thread)

        # 连接信号槽
        self.download_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_console)
        self.worker.result.connect(self._handle_download_result)
        self.worker.finished.connect(self.download_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.download_thread.finished.connect(self.download_thread.deleteLater)

        # 启动线程
        self.download_thread.start()
        self.update_console("后台下载线程已启动...")

    def _get_worker_count(self):
        """线程数校验"""
        try:
            return int(self.lineEdit_worker.text())
        except ValueError:
            self.update_console("线程数无效，使用默认值8")
            return 8

    def _generate_output_filename(self):
        """文件名生成（原有逻辑迁移）"""
        output_dir = "output"
        base_name = "outputfile"
        index = 1
        output_file = os.path.join(output_dir, f"{base_name}.txt")
        while os.path.exists(output_file):
            output_file = os.path.join(output_dir, f"{base_name}_{index}.txt")
            index += 1
        return output_file

    def _handle_download_result(self, result):
        """结果处理"""
        if result == 0:
            self.update_console("下载完成")
        elif result == -1:
            self.update_console("下载失败")
        else:
            self.update_console(f"部分失败，失败章节数: {result}")


class QtLogHandler(logging.Handler):
    """ 自定义日志处理器，通过Qt信号转发日志 """

    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        msg = self.format(record)
        self.signal.emit(msg)  # 通过信号转发格式化后的日志


class DownloadWorker(QtCore.QObject):
    # 定义线程信号
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(str)
    result = QtCore.pyqtSignal(int)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            downloader = novel_downloader_2.NovelDownloader(**self.params)
            ret = downloader.download_chapters()
            self.result.emit(ret)
        except Exception as e:
            self.progress.emit(f"线程异常: {str(e)}")
            self.result.emit(-1)
        finally:
            self.finished.emit()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()

    sys.exit(app.exec_())