from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QColor, QLinearGradient, QPainter


class GlassFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._blur_radius = 20
        self._opacity = 0.15
        self._gradient_start = QColor(255, 255, 255, 120)
        self._gradient_end = QColor(255, 255, 255, 50)
        self._border_width = 1
        self._border_color = QColor(255, 255, 255, 80)

        self.setup_effects()
        self.setAttribute(Qt.WA_Hover)

    def setup_effects(self):
        # 阴影效果
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

        # 鼠标悬停动画
        self.hover_anim = QPropertyAnimation(self, b"frameOpacity")
        self.hover_anim.setDuration(300)
        self.hover_anim.setEasingCurve(QEasingCurve.OutQuad)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制玻璃背景
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, self._gradient_start)
        gradient.setColorAt(1, self._gradient_end)

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 12, 12)

        # 绘制边框
        painter.setPen(QColor(self._border_color))
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 12, 12)

    def event(self, event):
        # 鼠标悬停动画处理
        if event.type() == event.HoverEnter:
            self.hover_anim.setStartValue(self._opacity)
            self.hover_anim.setEndValue(0.25)
            self.hover_anim.start()
        elif event.type() == event.HoverLeave:
            self.hover_anim.setStartValue(self._opacity)
            self.hover_anim.setEndValue(0.15)
            self.hover_anim.start()
        return super().event(event)

    # 支持QSS的自定义属性
    def getBlurRadius(self):
        return self._blur_radius

    def setBlurRadius(self, value):
        self._blur_radius = value
        self.shadow.setBlurRadius(value)
        self.update()

    def getFrameOpacity(self):
        return self._opacity

    def setFrameOpacity(self, value):
        self._opacity = value
        self._gradient_start.setAlpha(int(value * 255))
        self._gradient_end.setAlpha(int(value * 180))
        self.update()

    # 注册属性到QSS系统
    blurRadius = pyqtProperty(int, getBlurRadius, setBlurRadius)
    frameOpacity = pyqtProperty(float, getFrameOpacity, setFrameOpacity)
