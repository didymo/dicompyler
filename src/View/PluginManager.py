# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginManager.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView


class Ui_PluginManager(object):
    def setupUi(self, PluginManager):
        PluginManager.setObjectName("PluginManager")
        PluginManager.resize(766, 600)
        PluginManager.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(PluginManager)
        self.centralwidget.setObjectName("centralwidget")
        self.treeList = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeList.setGeometry(QtCore.QRect(10, 30, 261, 471))
        self.treeList.setStyleSheet("QTreeWidget::item {\n"
"    background-color: rgb(255, 255, 255);\n"
"  padding: 5px 0;\n"
"}")
        self.treeList.setObjectName("treeList")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeList)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeList)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setPointSize(12)
        item_1.setFont(0, font)
        self.optionTitle = QtWidgets.QLabel(self.centralwidget)
        self.optionTitle.setGeometry(QtCore.QRect(290, 50, 281, 31))
        self.optionTitle.setStyleSheet("font: 57 12pt \"Ubuntu\";")
        self.optionTitle.setObjectName("optionTitle")
        self.enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.enabled.setGeometry(QtCore.QRect(660, 60, 92, 23))
        self.enabled.setObjectName("enabled")
        self.content = QtWidgets.QWidget(self.centralwidget)
        self.content.setGeometry(QtCore.QRect(290, 90, 451, 411))
        self.content.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.content.setObjectName("content")
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(638, 554, 101, 31))
        self.cancel_button.setStyleSheet("background-color: rgb(238, 238, 236);\n"
"                                       font: 57 11pt \\\"Ubuntu\\\";\n"
"\n"
"                                       font-weight: bold;\n"
"color: rgb(85, 87, 83);")
        self.cancel_button.setObjectName("cancel_button")
        self.apply_button = QtWidgets.QPushButton(self.centralwidget)
        self.apply_button.setGeometry(QtCore.QRect(510, 554, 111, 31))
        self.apply_button.setStyleSheet("background-color: rgb(238, 238, 236);\n"
"                                       font: 57 11pt \\\"Ubuntu\\\";\n"
"                                       color:rgb(75,0,130);\n"
"                                       font-weight: bold;")
        self.apply_button.setObjectName("apply_button")
        PluginManager.setCentralWidget(self.centralwidget)

        self.retranslateUi(PluginManager)
        QtCore.QMetaObject.connectSlotsByName(PluginManager)

    def retranslateUi(self, PluginManager):
        _translate = QtCore.QCoreApplication.translate
        PluginManager.setWindowTitle(_translate("PluginManager", "Plugin Manager"))
        __sortingEnabled = self.treeList.isSortingEnabled()
        self.treeList.setSortingEnabled(False)
        self.treeList.expandAll()
        self.treeList.header().hide()
        self.treeList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeList.topLevelItem(0).setText(0, _translate("PluginManager", "Built-In Plugins"))
        self.treeList.topLevelItem(0).child(0).setText(0, _translate("PluginManager", "2D View"))
        self.treeList.topLevelItem(0).child(1).setText(0, _translate("PluginManager", "Anonymize"))
        self.treeList.topLevelItem(0).child(2).setText(0, _translate("PluginManager", "DVH"))
        self.treeList.topLevelItem(1).setText(0, _translate("PluginManager", "User Plugins"))
        self.treeList.topLevelItem(1).child(0).setText(0, _translate("PluginManager", "Image Windowing"))
        self.treeList.topLevelItem(1).child(1).setText(0, _translate("PluginManager", "Standard Organ Names"))
        self.treeList.topLevelItem(1).child(2).setText(0, _translate("PluginManager", "Standard Volume Names"))
        self.treeList.topLevelItem(1).child(3).setText(0, _translate("PluginManager", "Create ROI from Isodose"))
        self.treeList.topLevelItem(1).child(4).setText(0, _translate("PluginManager", "Patient ID - Hash ID"))
        self.treeList.setSortingEnabled(__sortingEnabled)
        self.optionTitle.setText(_translate("PluginManager", "TextLabel"))
        self.enabled.setText(_translate("PluginManager", "Enabled"))
        self.cancel_button.setText(_translate("PluginManager", "Cancel"))
        self.apply_button.setText(_translate("PluginManager", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginManager = QtWidgets.QMainWindow()
    ui = Ui_PluginManager()
    ui.setupUi(PluginManager)
    PluginManager.show()
    sys.exit(app.exec_())
