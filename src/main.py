from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from PyQt5.QtGui import QColor,QPixmap, QPainter
from picture_manager import BackgroundSetter
from src.windows2 import Ui_MainWindow
import novel_downloader_2
import os
import threading

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setupUi(self)  # Setup the UI from the imported class
        download_thread = threading.Thread(target=self.download_novel)

        #构件pushButton自定义
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))
        #图片构件自定义
        background_setter = BackgroundSetter(self.widget_toolbox_page1, "../QT/resource/tool_box_page1_background.png", 0.8)
        background_setter = BackgroundSetter(self.label, "../QT/resource/label_2.png", 0.3)
        background_setter = BackgroundSetter(self.frame_MainBackground, "../QT/resource/image.png", 0.9)
        background_setter = BackgroundSetter(self.frame_7, "../QT/resource/frame_7.png", 0.4)
        background_setter = BackgroundSetter(self.frame_9, "../QT/resource/frame_9.png", 0.4)
        self.pushButton_downloader.clicked.connect(self.download_novel)
    def update_console(self, message):
        self.plainTextEdit_console.appendPlainText(message)

    def download_novel(self):
        def generate_output_file_name(output_dir, base_name="outputfile"):
            index = 1
            output_file = os.path.join(output_dir, f"{base_name}.txt")

            while os.path.exists(output_file):
                output_file = os.path.join(output_dir, f"{base_name}_{index}.txt")
                index += 1

            return output_file
        baseurl = self.line_edit_baseurl.text()


        url_path = self.lineEdit_urlpath.text()
        selector_chapterList = self.lineEdit_chapterListSelector.text()
        selector_content = self.lineEdit_contentSelector.text()
        output_dir = "output"
        output_file = generate_output_file_name(output_dir)
        max_workers = self.lineEdit_worker.text()
        self.update_console("Download started...")
        try:
            max_workers = int(self.lineEdit_worker.text())
        except ValueError:
            self.update_console("线程数必须是整数")
            return
        downloader = novel_downloader_2.NovelDownloader(
            baseurl=baseurl,
            url_path=url_path,
            output_file=output_file,
            selector_content=selector_content,
            selector_chapter=selector_chapterList,
            max_workers=max_workers
        )
        result = downloader.download_chapters()
        if result == 0:
            self.update_console("下载完成")
        elif result == -1:
            self.update_console("下载失败")
        else:
            self.update_console(f"下载失败章节数: {result}")













if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())