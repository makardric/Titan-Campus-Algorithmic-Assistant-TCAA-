# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TitanAppLlNoLg.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1283, 785)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_frame = QFrame(self.centralwidget)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(-10, 0, 1280, 720))
        self.main_frame.setStyleSheet(u"background-color:  rgb(255, 255, 255)")
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.logo_image = QLabel(self.main_frame)
        self.logo_image.setObjectName(u"logo_image")
        self.logo_image.setGeometry(QRect(150, 150, 391, 381))
        self.logo_image.setPixmap(QPixmap(u"resources/csuf logo.png"))
        self.logo_image.setScaledContents(True)
        self.title_label = QLabel(self.main_frame)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(550, 260, 331, 101))
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"color: #00274c")
        self.title_label.setWordWrap(True)
        self.text_label = QLabel(self.main_frame)
        self.text_label.setObjectName(u"text_label")
        self.text_label.setGeometry(QRect(630, 360, 121, 21))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.text_label.setFont(font1)
        self.text_label.setStyleSheet(u"color: #e17000")
        self.button_frame = QFrame(self.main_frame)
        self.button_frame.setObjectName(u"button_frame")
        self.button_frame.setGeometry(QRect(1140, 0, 141, 721))
        self.button_frame.setStyleSheet(u"background-color: #00274c")
        self.button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.button_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.button_logo__image = QLabel(self.button_frame)
        self.button_logo__image.setObjectName(u"button_logo__image")
        self.button_logo__image.setGeometry(QRect(20, 20, 101, 111))
        self.button_logo__image.setPixmap(QPixmap(u"resources/titans logo.png"))
        self.button_logo__image.setScaledContents(True)
        self.verticalLayoutWidget = QWidget(self.button_frame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(-1, 159, 146, 561))
        self.button_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.button_layout.setSpacing(0)
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setBold(True)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setAutoFillBackground(False)

        self.button_layout.addWidget(self.pushButton_2)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setFont(font2)

        self.button_layout.addWidget(self.pushButton_5)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setFont(font2)

        self.button_layout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setFont(font2)

        self.button_layout.addWidget(self.pushButton_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1283, 33))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo_image.setText("")
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"Titan Campus Algorithmic Assistant", None))
        self.text_label.setText(QCoreApplication.translate("MainWindow", u"CSUF made easy.", None))
        self.button_logo__image.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"CAMPUS NAVIGATOR", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"STUDY PLANNER", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"NOTES SEARCH ENGINE", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"ALGORITHM INFO", None))
    # retranslateUi

