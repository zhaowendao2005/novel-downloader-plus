import sys
from pathlib import Path
import src
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from src.picture_manager import BackgroundSetter
from src.qt.windows2 import Ui_MainWindow
from PyQt5.QtGui import QMouseEvent
from src.downloader import novel_downloader_2
import threading
import logging
import os

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def open_output_file():
    os.startfile("file_output")
    #日志输出函数


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
        background_setter = BackgroundSetter(self.widget_toolbox_page1, "assets/tool_box_page1_background.png", 0.8)
        background_setter = BackgroundSetter(self.label, "assets/label_2.png", 0.3)
        background_setter = BackgroundSetter(self.frame_MainBackground, "assets/image.png", 0.9)
        background_setter = BackgroundSetter(self.frame_7, "assets/frame_7.png", 0.4)
        background_setter = BackgroundSetter(self.frame_9, "assets/frame_9.png", 0.4)
        self.pushButton_downloader.clicked.connect(self.download_novel)
        self.toolButton_exitWindow.clicked.connect(self.close)
        self.toolButton_removeWindow.clicked.connect(self.showMinimized)
        self.toolButton_maximiseWindow.clicked.connect(self.showMaximized)
        self.pushButton_openOutPut.clicked.connect(open_output_file)
        self.pushButton_stop.clicked.connect(self.stop_download)
            #强制终止任务方法
    def stop_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.update_console("正在安全终止下载...")
            self.download_timer.stop()
        if self.download_thread and self.download_thread.isRunning():
            self.update_console("正在安全终止下载...")
            # 先请求正常退出
            self.download_thread.requestInterruption()
            self.worker.interrupt_requested = True  # 需要给worker添加中断标志

            # 设置超时强制终止
            if not self.download_thread.wait(3000):  # 等待3秒
                self.update_console("强制终止线程...")
                self.download_thread.terminate()
                if not self.download_thread.wait(1000):
                    self.update_console("线程终止失败")
            self._cleanup_thread()

    #资源管理器打开存储目录
    def open_output_file(self):
        os.statvfs("file_output")
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

    def _cleanup_thread(self):
        try:
            if self.download_thread:
                self.download_thread.quit()
                self.download_thread.wait()
                self.download_thread.deleteLater()
            if self.worker:
                self.worker.deleteLater()
        except RuntimeError:
            pass
        finally:
            self.download_thread = None
            self.worker = None

    def download_novel(self):
        """重构后的下载方法"""
        if self.download_thread and self.download_thread.isRunning():
            self.update_console("下载正在进行中...")
            return

        # 在原来的代码之后增加超时检测
        self.download_timer = QtCore.QTimer()
        self.download_timer.timeout.connect(self.check_thread_status)
        self.download_timer.start(5000)  # 每5秒检测一次





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
        self.worker.finished.connect(self._cleanup_thread)

        # 启动线程
        self.download_thread.start()
        self.update_console("后台下载线程已启动...")
        #强制终止任务时检测对象是否存在
    def check_thread_status(self):
        if self.download_thread is None:  # 新增检查
            self.download_timer.stop()
            return
        if not self.download_thread.isRunning():
            self.update_console("线程已终止，正在清理...")
            self._cleanup_thread()
            self.download_timer.stop()
        if not self.download_thread.isRunning():
            self.update_console("线程已终止，正在清理...")
            self._cleanup_thread()
            self.download_timer.stop()
        else:
            self.download_timer.stop()
    def _get_worker_count(self):
        """线程数校验"""
        try:
            return int(self.lineEdit_worker.text())
        except ValueError:
            self.update_console("线程数无效，使用默认值8")
            return 8

    def _generate_output_filename(self):
        """文件名生成（原有逻辑迁移）"""
        output_dir = "file_output"
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
        self.interrupt_requested = False  # 新增中断标志

    def run(self):
        try:
            downloader = novel_downloader_2.NovelDownloader(**self.params)
            ret = downloader.download_chapters()
            self.result.emit(ret)
        except Exception as e:
            logging.exception("Download failed")
            self.progress.emit(f"线程异常: {str(e)}")
            self.result.emit(-1)
        finally:
            try:
                self.finished.emit()
            except RuntimeError:  # 处理对象已删除的情况
                pass

    def check_interrupt(self):
        """ 供downloader调用的中断检查 """
        return self.interrupt_requested or self.thread().isInterruptionRequested()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()

    sys.exit(app.exec_())