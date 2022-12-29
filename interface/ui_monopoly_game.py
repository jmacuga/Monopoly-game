# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'monopoly_game.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1151, 857)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setAutoFillBackground(False)
        self.label_9.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 3, 2, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 3, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_5.setTextFormat(Qt.RichText)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"QLabel{\n"
                                 "background: rgb(191, 219, 174)\n"
                                 "}")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel{\n"
                                   "background: rgb(191, 219, 174)\n"
                                   "}")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1151, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_6.setText("")
        self.label_4.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
    # retranslateUi
