# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'janelaCadastro.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(525, 176)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 30, 47, 13))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 70, 47, 13))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 110, 47, 13))
        self.editNome = QLineEdit(Form)
        self.editNome.setObjectName(u"editNome")
        self.editNome.setGeometry(QRect(100, 30, 401, 20))
        self.editTelefone = QLineEdit(Form)
        self.editTelefone.setObjectName(u"editTelefone")
        self.editTelefone.setGeometry(QRect(100, 70, 401, 20))
        self.editEmail = QLineEdit(Form)
        self.editEmail.setObjectName(u"editEmail")
        self.editEmail.setGeometry(QRect(100, 110, 401, 20))
        self.botaoOk = QPushButton(Form)
        self.botaoOk.setObjectName(u"botaoOk")
        self.botaoOk.setGeometry(QRect(310, 140, 75, 23))
        self.botaooCancelar = QPushButton(Form)
        self.botaooCancelar.setObjectName(u"botaooCancelar")
        self.botaooCancelar.setGeometry(QRect(400, 140, 75, 23))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Nome", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Telefone", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Email", None))
        self.editTelefone.setInputMask(QCoreApplication.translate("Form", u"(00) 00000-0000", None))
        self.botaoOk.setText(QCoreApplication.translate("Form", u"OK", None))
        self.botaooCancelar.setText(QCoreApplication.translate("Form", u"Cancelar", None))
    # retranslateUi

