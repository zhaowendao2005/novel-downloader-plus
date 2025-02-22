from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from PyQt5.QtGui import QColor,QPixmap, QPainter
from picture_manager import BackgroundSetter
from src.windows2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setupUi(self)  # Setup the UI from the imported class

        #构件pushButton自定义
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))
        #图片构件自定义
        background_setter = BackgroundSetter(self.widget_toolbox_page1, "../QT/resource/tool_box_page1_background.png", 0.8)
        background_setter = BackgroundSetter(self.label, "../QT/resource/label_2.png", 0.3)
        background_setter = BackgroundSetter(self.frame_MainBackground, "../QT/resource/image.png", 0.9)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())