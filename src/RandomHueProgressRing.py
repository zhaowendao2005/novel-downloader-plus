import random
from PyQt5.QtGui import QColor
from qfluentwidgets import IndeterminateProgressRing


class RandomHueProgressRing(IndeterminateProgressRing):
    """ 随机色相+角度联动的进度环 """

    def __init__(self, parent=None, start=True):
        super().__init__(parent=parent, start=start)

        # 初始随机基色（色相值 0-360）
        self.base_hue = random.randint(0, 360)

        self.startAngle = 0
        self.spanAngle = 360

        # 每完成一个动画循环更换基色
        self.aniGroup.currentLoopChanged.connect(self._randomizeBaseHue)


    def setProgressRingLength(self, start_angle, span_angle):
        """ 设置进度环的起始角度和跨度角度 """
        self.startAngle = start_angle
        self.spanAngle = span_angle
        self.update()  # 更新进度环显示

    def _randomizeBaseHue(self):
        """ 随机生成新的基色 """
        self.base_hue = random.randint(0, 360)

    def lightBarColor(self):
        # 亮色模式：高亮度
        return self._calculateColor(lightness=255)

    def darkBarColor(self):
        # 暗色模式：中等亮度
        return self._calculateColor(lightness=180)

    def _calculateColor(self, lightness):
        """ 根据当前角度计算颜色 """
        # 动态色相 = 基色 + 旋转角度（取模360）
        dynamic_hue = (self.base_hue + self.startAngle) % 360

        # HSV 转 QColor（H:0-359, S:100%, V:按主题亮度）
        return QColor.fromHsv(
            dynamic_hue,  # 色相（0-359）
            255,  # 饱和度（0-255）
            lightness,  # 亮度（0-255）
            200  # 透明度（200为半透明效果）
        )
