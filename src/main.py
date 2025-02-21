from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import FluentIcon, setTheme
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from PyQt5.QtGui import QColor,QPixmap, QPainter, QImage

from QT.main_window.windows1 import Ui_MainWindow
from qfluentwidgets.components import PushButton
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setupUi(self)  # Setup the UI from the imported class
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))
        self.setImageWithOpacity('../QT/resource/image.PNG', 0.3)

    def setImageWithOpacity(self, imagePath: str, opacity: float):
        """ Set the image with specified opacity and scale it with the window size """
        pixmap = QPixmap(imagePath)
        if not pixmap.isNull():
            image = pixmap.toImage()
            painter = QPainter(image)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            painter.fillRect(image.rect(), QColor(0, 0, 0, int(255 * opacity)))
            painter.end()
            scaled_pixmap = QPixmap.fromImage(image).scaled(self.label_2.size(), QtCore.Qt.KeepAspectRatio,
                                                            QtCore.Qt.SmoothTransformation)
            self.label_2.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())