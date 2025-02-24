from PyQt5.QtWidgets import QLabel, QGraphicsBlurEffect, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap


class GlassLabel(QLabel):
    def __init__(self, parent=None):
        super(GlassLabel, self).__init__(parent)

        # 必需设置
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # 设置默认样式
        self.setStyleSheet("color: white; font-size: 20px;")

    def paintEvent(self, event):
        # 创建临时绘图设备
        bg_pixmap = QPixmap(self.size())
        bg_pixmap.fill(Qt.transparent)

        # 绘制背景到临时pixmap
        bg_painter = QPainter(bg_pixmap)
        bg_painter.setRenderHint(QPainter.Antialiasing)
        bg_painter.setBrush(QColor(255, 255, 255, 120))
        bg_painter.setPen(Qt.NoPen)
        bg_pixmap_rect = self.rect()
        bg_painter.drawRoundedRect(bg_pixmap_rect, 10, 10)
        bg_painter.end()

        # 创建模糊效果
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(bg_pixmap)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)  # 可调整模糊程度
        item.setGraphicsEffect(blur_effect)
        scene.addItem(item)

        # 渲染模糊后的背景
        blurred_pixmap = QPixmap(self.size())
        blurred_pixmap.fill(Qt.transparent)
        blur_painter = QPainter(blurred_pixmap)
        scene.render(blur_painter)
        blur_painter.end()

        # 主绘制器
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制模糊背景
        painter.drawPixmap(0, 0, blurred_pixmap)

        # 绘制清晰文字
        painter.setPen(Qt.white)
        painter.setFont(self.font())  # 继承样式表设置的字体
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())
