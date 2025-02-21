from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
w = AcrylicLabel(20, QColor(105, 114, 168, 102))
w.setImage('resource/埃罗芒阿老师.jpg')
w.show()
app.exec_()