import json
from typing import Dict, Any
from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QLinearGradient, QPainter


class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def load_config(cls, filepath: str = "style_config.json"):
        """Load style configuration from JSON file"""
        try:
            with open(filepath, "r") as f:
                cls._config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            cls._config = {}

    @classmethod
    def get_style(cls, widget_type: str, instance_id: str) -> Dict[str, Any]:
        """Get style parameters for specific widget instance"""
        return cls._config.get(widget_type, {}).get(instance_id, {})


class GlassFrame(QFrame):
    def __init__(self, instance_id: str = "default", parent=None):
        super().__init__(parent)
        self.instance_id = instance_id
        self._load_style_config()
        self.setup_effects()
        self.setAttribute(Qt.WA_Hover)

    def _load_style_config(self):
        """Load style parameters from configuration"""
        style = ConfigManager.get_style("GlassFrame", self.instance_id)

        # Background parameters
        self._opacity = style.get("opacity", 0.15)
        self._gradient_start = self._parse_color(style.get("gradient_start"),
                                                 QColor(255, 255, 255, 120))
        self._gradient_end = self._parse_color(style.get("gradient_end"),
                                               QColor(255, 255, 255, 50))

        # Border parameters
        self._border_width = style.get("border_width", 1)
        self._border_color = self._parse_color(style.get("border_color"),
                                               QColor(255, 255, 255, 80))

        # Shadow parameters
        shadow_config = style.get("shadow", {})
        self.shadow_blur = shadow_config.get("blur_radius", 30)
        self.shadow_color = self._parse_color(shadow_config.get("color"),
                                              QColor(0, 0, 0, 80))
        self.shadow_offset = shadow_config.get("offset", (0, 4))

        # Animation parameters
        anim_config = style.get("hover_animation", {})
        self.anim_duration = anim_config.get("duration", 300)
        self.easing_curve = getattr(QEasingCurve,
                                    anim_config.get("easing_curve", "OutQuad"),
                                    QEasingCurve.OutQuad)
        self.hover_enter_opacity = anim_config.get("enter_opacity", 0.25)
        self.hover_leave_opacity = anim_config.get("leave_opacity", 0.15)

    def _parse_color(self, color_data, default: QColor) -> QColor:
        """Parse color data from config to QColor"""
        if isinstance(color_data, list) and len(color_data) >= 3:
            alpha = color_data[3] if len(color_data) > 3 else default.alpha()
            return QColor(*color_data[:3], alpha)
        return default

    def setup_effects(self):
        # 配置阴影视效
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(self.shadow_blur)
        self.shadow.setColor(self.shadow_color)
        self.shadow.setOffset(*self.shadow_offset)
        self.setGraphicsEffect(self.shadow)

        # 配置悬停动画
        self.hover_anim = QPropertyAnimation(self, b"opacity")
        self.hover_anim.setDuration(self.anim_duration)
        self.hover_anim.setEasingCurve(self.easing_curve)

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
        # 处理悬停动画
        if event.type() == event.HoverEnter:
            self.hover_anim.setStartValue(self._opacity)
            self.hover_anim.setEndValue(self.hover_enter_opacity)
            self.hover_anim.start()
        elif event.type() == event.HoverLeave:
            self.hover_anim.setStartValue(self._opacity)
            self.hover_anim.setEndValue(self.hover_leave_opacity)
            self.hover_anim.start()
        return super().event(event)

    # 属性访问器用于动画系统
    def get_opacity(self) -> float:
        return self._opacity

    def set_opacity(self, value: float):
        self._opacity = value
        self._gradient_start.setAlpha(int(value * 255))
        self._gradient_end.setAlpha(int(value * 180))
        self.update()

    opacity = property(get_opacity, set_opacity)
