# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calculadora.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 559)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(300, 400))
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #2d1f3d,\n"
"        stop:1 #1a1a2e);\n"
"}\n"
"\n"
"QPushButton {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0.0 #ff3366,    /* Vermelho rosado */\n"
"        stop:0.2 #ff9933,    /* Laranja suave */\n"
"        stop:0.4 #ffcc33,    /* Amarelo dourado */\n"
"        stop:0.6 #33cc33,    /* Verde esmeralda */\n"
"        stop:0.8 #3366ff,    /* Azul royal */\n"
"        stop:1.0 #9933ff);   /* Roxo vibrante */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border: 1px solid rgba(255, 255, 255, 0.2);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0.0 #ff4d77,\n"
"        stop:0.2 #ffad4d,\n"
"        stop:0.4 #ffd24d,\n"
"        stop:0.6 #4dd24d,\n"
"        stop:0.8 #4d77ff,\n"
"        stop:1.0 #ad4dff);\n"
"}\n"
"\n"
"QLin"
                        "eEdit {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #2e2e4a,\n"
"        stop:1 #3d2e4a);\n"
"    color: #e0e0e0;\n"
"    border: 2px solid #4a3d5a;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QListWidget {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #2e2e4a,\n"
"        stop:1 #3d2e4a);\n"
"    color: #e0e0e0;\n"
"    border: 2px solid #4a3d5a;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.listWidget.setStyleSheet(u"")

        self.gridLayout.addWidget(self.listWidget, 0, 1, 1, 4)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy1.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_7, 7, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy1.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_5, 5, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy1.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_4, 5, 4, 1, 1)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_3, 6, 4, 1, 1)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_6, 6, 2, 1, 1)

        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy1.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_8, 8, 1, 1, 1)

        self.pushButton_10 = QPushButton(self.centralwidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy1.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_10, 8, 2, 1, 1)

        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy1.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_9, 7, 2, 1, 1)

        self.butaoIgual = QPushButton(self.centralwidget)
        self.butaoIgual.setObjectName(u"butaoIgual")
        sizePolicy1.setHeightForWidth(self.butaoIgual.sizePolicy().hasHeightForWidth())
        self.butaoIgual.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.butaoIgual, 8, 4, 2, 1)

        self.pushButton_12 = QPushButton(self.centralwidget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        sizePolicy1.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_12, 5, 2, 1, 1)

        self.pushButton_16 = QPushButton(self.centralwidget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy1.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_16, 8, 3, 1, 1)

        self.pushButton_15 = QPushButton(self.centralwidget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy1.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_15, 7, 3, 1, 1)

        self.pushButton_14 = QPushButton(self.centralwidget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy1.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_14, 6, 3, 1, 1)

        self.pushButton_13 = QPushButton(self.centralwidget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy1.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_13, 6, 1, 1, 1)

        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        sizePolicy1.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_11, 5, 3, 1, 1)

        self.pushButton_17 = QPushButton(self.centralwidget)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy1.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_17, 9, 2, 1, 1)

        self.botaoC = QPushButton(self.centralwidget)
        self.botaoC.setObjectName(u"botaoC")
        sizePolicy1.setHeightForWidth(self.botaoC.sizePolicy().hasHeightForWidth())
        self.botaoC.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.botaoC, 7, 4, 1, 1)

        self.pushButton_18 = QPushButton(self.centralwidget)
        self.pushButton_18.setObjectName(u"pushButton_18")
        sizePolicy1.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_18, 9, 3, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton, 9, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 4, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 760, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.butaoIgual.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"*", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.botaoC.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u",", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"+/-", None))
    # retranslateUi

