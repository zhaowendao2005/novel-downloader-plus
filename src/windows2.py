# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows2.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 477)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("Qcentralwidget=rgba(255, 255, 255, 0)")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_MainBackground = QtWidgets.QFrame(self.centralwidget)
        self.frame_MainBackground.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"")
        self.frame_MainBackground.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_MainBackground.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_MainBackground.setObjectName("frame_MainBackground")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_MainBackground)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label_title = QtWidgets.QLabel(self.frame_MainBackground)
        self.label_title.setStyleSheet("background-color: rgba(59, 59, 59, 200);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_6.addWidget(self.label_title)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout_12.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.frame_7 = GlassFrame(self.frame_MainBackground)
        self.frame_7.setStyleSheet("border-radius: 18px;\n"
"background-color: rgb(110, 112, 0,0);\n"
"        qproperty-gradientAngle: 45;\n"
"        qproperty-borderColor: rgba(200, 220, 255, 150);\n"
"        qproperty-shadowColor: rgba(100, 120, 150, 80);\n"
"        qproperty-shadowBlur: 40;\n"
"        qproperty-hoverAnimDuration: 500;\n"
"        qproperty-glassOpacity: 0.25;\n"
"\n"
"")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.toolBox = QtWidgets.QToolBox(self.frame_7)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 128, 266))
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_toolbox_page1 = QtWidgets.QWidget(self.page)
        self.widget_toolbox_page1.setStyleSheet("")
        self.widget_toolbox_page1.setObjectName("widget_toolbox_page1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_toolbox_page1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2.addWidget(self.widget_toolbox_page1)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 128, 266))
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = GlassFrame(self.page_2)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2.addWidget(self.frame)
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout.addWidget(self.toolBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_11.addWidget(self.frame_7)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.frame_8 = GlassFrame(self.frame_MainBackground)
        self.frame_8.setStyleSheet("        qproperty-gradientAngle: 45;\n"
"        qproperty-borderColor: rgba(200, 220, 255, 150);\n"
"        qproperty-shadowColor: rgba(100, 120, 150, 80);\n"
"        qproperty-shadowBlur: 40;\n"
"        qproperty-hoverAnimDuration: 500;\n"
"        qproperty-glassOpacity: 0.25;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_8)
        self.stackedWidget.setStyleSheet("Qframe#frame9")
        self.stackedWidget.setObjectName("stackedWidget")
        self.contentPage1 = QtWidgets.QWidget()
        self.contentPage1.setObjectName("contentPage1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.contentPage1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_9 = QtWidgets.QFrame(self.contentPage1)
        self.frame_9.setStyleSheet("")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.frame_9)
        self.plainTextEdit_3.setStyleSheet("background-color: rgba(100, 100, 100, 150);\n"
"border-radius: 18px;")
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setCenterOnScroll(False)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.horizontalLayout_15.addWidget(self.plainTextEdit_3)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_12 = LineEdit(self.frame_9)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout_3.addWidget(self.lineEdit_12, 1, 1, 1, 1)
        self.lineEdit_11 = LineEdit(self.frame_9)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout_3.addWidget(self.lineEdit_11, 2, 1, 1, 1)
        self.pushButton_downloader = PushButton(self.frame_9)
        self.pushButton_downloader.setObjectName("pushButton_downloader")
        self.gridLayout_3.addWidget(self.pushButton_downloader, 2, 0, 1, 1)
        self.lineEdit_10 = LineEdit(self.frame_9)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout_3.addWidget(self.lineEdit_10, 3, 1, 1, 1)
        self.lineEdit_9 = LineEdit(self.frame_9)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout_3.addWidget(self.lineEdit_9, 0, 1, 1, 1)
        self.verticalLayout_18.addLayout(self.gridLayout_3)
        self.label = QtWidgets.QLabel(self.frame_9)
        self.label.setStyleSheet("border-radius: 30px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_18.addWidget(self.label)
        self.verticalLayout_15.addLayout(self.verticalLayout_18)
        self.verticalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.addLayout(self.verticalLayout_15)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_7.addWidget(self.frame_9)
        self.stackedWidget.addWidget(self.contentPage1)
        self.contentPage2 = QtWidgets.QWidget()
        self.contentPage2.setObjectName("contentPage2")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.contentPage2)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.pushButton_6 = QtWidgets.QPushButton(self.contentPage2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_13.addWidget(self.pushButton_6)
        self.stackedWidget.addWidget(self.contentPage2)
        self.verticalLayout_17.addWidget(self.stackedWidget)
        self.horizontalLayout_9.addLayout(self.verticalLayout_17)
        self.horizontalLayout_11.addWidget(self.frame_8)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(2, 4)
        self.verticalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_12.setStretch(0, 1)
        self.verticalLayout_12.setStretch(1, 10)
        self.horizontalLayout_12.addLayout(self.verticalLayout_12)
        self.verticalLayout_11.addWidget(self.frame_MainBackground)
        self.horizontalLayout_10.addLayout(self.verticalLayout_11)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.toolBox.currentChanged['int'].connect(self.stackedWidget.setCurrentIndex) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "小说下载器"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Page 1"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Page 2"))
        self.pushButton_downloader.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
from GlassFrame import GlassFrame
from qfluentwidgets import LineEdit, PushButton
import resource_rc
