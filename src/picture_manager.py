from PyQt5 import QtCore, QtWidgets, QtGui

class BackgroundSetter:
    def __init__(self, widget: QtWidgets.QWidget, imagePath: str, opacity: float = 1.0):
        self.widget = widget
        self.imagePath = imagePath
        self.opacity = opacity
        self.bg_label = QtWidgets.QLabel(widget)
        self.setupBackground()

    def setupBackground(self):
        """Set up the background image with specified opacity and scaling."""
        self.bg_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)  # Allow mouse events to pass through
        self.bg_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.bg_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the image

        # Set opacity effect
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(self.opacity)
        self.bg_label.setGraphicsEffect(opacity_effect)

        # Load and set the image
        pixmap = QtGui.QPixmap(self.imagePath)
        if not pixmap.isNull():
            self.updatePixmap(pixmap)
            self.widget.resizeEvent = lambda event: self.updatePixmap(pixmap)

        # Ensure the background is at the lowest layer
        self.bg_label.lower()
        # Allow the widget to auto-fill the background (avoid transparency issues)
        self.widget.setAutoFillBackground(True)

    def updatePixmap(self, pixmap):
        """Update the pixmap to fit the widget size."""
        scaled = pixmap.scaled(
            self.widget.size(),
            QtCore.Qt.KeepAspectRatioByExpanding,  # Maintain aspect ratio
            QtCore.Qt.SmoothTransformation
        )
        self.bg_label.setPixmap(scaled)
        self.bg_label.setGeometry(0, 0, self.widget.width(), self.widget.height())  # Cover the entire widget\
        # Example usage #示例代码
        if __name__ == "__main__":
            import sys
            app = QtWidgets.QApplication(sys.argv)
            main_window = QtWidgets.QMainWindow()
            central_widget = QtWidgets.QWidget(main_window)
            main_window.setCentralWidget(central_widget)

            # Set background
            background_setter = BackgroundSetter(central_widget, "../QT/resource/tool_box_page1_background.png", 0.5)

            main_window.show()
            sys.exit(app.exec_())