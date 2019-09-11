# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_page.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class WelcomePage(object):
    def setupUi(self, WelcomePage):
        WelcomePage.setObjectName("WelcomePage")
        WelcomePage.resize(844, 528)
        WelcomePage.setStyleSheet("background-color: rgb(244, 245, 245);")
        self.centralwidget = QtWidgets.QWidget(WelcomePage)
        self.centralwidget.setObjectName("centralwidget")
        self.welcomeLabel = QtWidgets.QLabel(self.centralwidget)
        self.welcomeLabel.setGeometry(QtCore.QRect(310, 310, 201, 41))
        self.welcomeLabel.setStyleSheet("font: 57 18pt \"Ubuntu\";\n"
        "font: 57 18pt \"Ubuntu\";")
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 360, 521, 21))
        self.label_2.setStyleSheet("font: 57 12pt \"Ubuntu\";")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 410, 121, 31))
        self.pushButton.setStyleSheet("font: 57 12pt \"Ubuntu\";color: rgb(244, 245, 245);\n"
        "font: 57 12pt \"Ubuntu\";\n"
        "background-color: rgb(147, 112, 219);")
        self.pushButton.setObjectName("pushButton")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(80, 30, 671, 261))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("src/Icon/logo.png"))
        self.logo.setObjectName("logo")
        WelcomePage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WelcomePage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 22))
        self.menubar.setObjectName("menubar")
        WelcomePage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WelcomePage)
        self.statusbar.setObjectName("statusbar")
        WelcomePage.setStatusBar(self.statusbar)

        self.retranslateUi(WelcomePage)
        QtCore.QMetaObject.connectSlotsByName(WelcomePage)

    def retranslateUi(self, WelcomePage):
        _translate = QtCore.QCoreApplication.translate
        WelcomePage.setWindowTitle(_translate("WelcomePage", "WelcomePage"))
        self.welcomeLabel.setText(_translate("WelcomePage", "Welcome to Onko!"))
        self.label_2.setText(_translate("WelcomePage", "To get started, upload a patient file and a clinical spreadsheet (optional)."))
        self.pushButton.setText(_translate("WelcomePage", "Open Patient"))

