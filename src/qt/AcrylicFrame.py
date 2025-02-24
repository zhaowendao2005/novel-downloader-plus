from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGraphicsBlurEffect


class AcrylicFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # 创建模糊效果
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(15)  # 调整模糊强度
        self.setGraphicsEffect(blur)
