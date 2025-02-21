from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import FluentIcon
from qfluentwidgets.common import Icon
from qfluentwidgets import setTheme, Theme
from PyQt5.QtGui import QColor,QPixmap, QPainter

from src.windows2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setupUi(self)  # Setup the UI from the imported class
        self.pushButton_downloader.setIcon(Icon(FluentIcon.DOWN))

        from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
        self.label_title = QtWidgets.QLabel(self.frame_MainBackground)
        self.label_title = AcrylicLabel(self.frame_MainBackground,tintColor=QColor(128, 138, 135, 102))
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_6.addWidget(self.label_title)
        self.label_2 = AcrylicLabel(self.contentPage1, tintColor=QColor(105, 114, 168, 102))
        self.label_2 = AcrylicLabel(5, QColor(255, 255, 255, 3))
        self.label_2.setText("")
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 4, 0, 1, 1)
        self.setImageWithOpacity('../QT/resource/image.PNG', 0.8)
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