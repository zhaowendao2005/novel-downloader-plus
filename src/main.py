from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon


from QT.main_window.windows1 import Ui_MainWindow
from qfluentwidgets.components import PushButton
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the imported class
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())