from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from QT.main_window.windows_glass import Ui_MainWindow
from src.novel_downloader_2 import NovelDownloader

# 添加路径自动补全依赖
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QDir
import time



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the imported class


        self.pushButton_selectSaveList.clicked.connect(self.select_save_list)
        self.pushButton_download.clicked.connect(self.download)#绑定下载按钮
    def download(self):
        baseurl = self.lineEdit_baseurl.text()
        url_path = self.lineEdit_chapterList_path.text()
        output_file = self.lineEdit_fileSavePath.text() or "output/novel_unfinished.txt"
        selector_content = self.lineEdit_chapterContentSelector.text()
        selector_chapter = self.lineEdit_chapterListSelector.text()
        max_workers = self.lineEdit_max_workers.text()
        # 添加参数验证
        if not all([baseurl, url_path, selector_chapter, selector_content]):
            self.plainTextEdit_logOutput("所有参数必须填写！", "red")
            return
        downloader = NovelDownloader(baseurl, url_path, output_file, selector_content, selector_chapter, max_workers)
        failed_chapters = downloader.download_chapters()
        if failed_chapters == -1:
            self.plainTextEdit_logOutput.showMessage("下载失败，查看日志以获取更多信息")
        elif failed_chapters:
            self.plainTextEdit_logOutput.showMessage(f"下载完成，有 {failed_chapters} 章下载失败")
        else:
            self.plainTextEdit_logOutput.showMessage("下载完成，所有章节下载成功")

    def log_output(self, message):
        self.plainTextEdit_logOutput.appendPlainText(f"[{QtCore.QDateTime.currentDateTime().toString()}] {message}")

    def select_save_list(self):#选择保存目录并行将保存目录填入文本框lineedit_fileSavePath
        # 添加默认路径记忆功能
        last_path = self.lineEdit_fileSavePath.text() or QtCore.QDir.homePath()

        directory = QFileDialog.getExistingDirectory(
            self,
            "选择保存目录",
            last_path,  # 记住上次路径
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if directory:
            self.lineEdit_fileSavePath.setText(directory)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())