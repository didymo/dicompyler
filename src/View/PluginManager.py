from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginManager(object):
    def setupUi(self, PluginManager):
        PluginManager.setObjectName("PluginManager")
        PluginManager.resize(766, 600)
        PluginManager.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(PluginManager)
        self.centralwidget.setObjectName("centralwidget")
        self.optionTitle = QtWidgets.QLabel(self.centralwidget)
        self.optionTitle.setGeometry(QtCore.QRect(290, 50, 281, 31))
        self.optionTitle.setStyleSheet("font: 57 12pt \"Ubuntu\";\n"
                                       "font-weight: bold;")
        self.optionTitle.setObjectName("optionTitle")
        self.enabled = QtWidgets.QCheckBox(self.centralwidget)
        self.enabled.setGeometry(QtCore.QRect(660, 60, 92, 23))
        self.enabled.setObjectName("enabled")
        self.table_modules = QtWidgets.QTableWidget(self.centralwidget)
        self.table_modules.setGeometry(QtCore.QRect(290, 90, 451, 370))
        self.table_modules.setObjectName("table_modules")
        self.table_modules.setStyleSheet("background-color: rgb(255, 255, 255);")
        #buttons per view
        self.add_new_window = QtWidgets.QPushButton(self.centralwidget)
        self.add_new_window.setGeometry(QtCore.QRect(598, 470, 141, 31))
        self.add_new_window.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                        "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                        "                                       color:rgb(75,0,130);\n"
                                        "                                       font-weight: bold;")
        self.add_new_window.setObjectName("add_new_window")
        self.add_new_window.setVisible(False)
        #organ
        self.add_standard_organ_name = QtWidgets.QPushButton(self.centralwidget)
        self.add_standard_organ_name.setGeometry(QtCore.QRect(578, 470, 161, 31))
        self.add_standard_organ_name.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                          "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                          "                                       color:rgb(75,0,130);\n"
                                          "                                       font-weight: bold;")
        self.add_standard_organ_name.setObjectName("add_standard_organ_name")
        self.add_standard_organ_name.setVisible(False)

        self.import_organ_csv = QtWidgets.QPushButton(self.centralwidget)
        self.import_organ_csv.setGeometry(QtCore.QRect(406, 470, 161, 31))
        self.import_organ_csv.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                                   "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                                   "                                       color:rgb(75,0,130);\n"
                                                   "                                       font-weight: bold;")
        self.import_organ_csv.setObjectName("import_organ_csv")
        self.import_organ_csv.setVisible(False)

        #volume
        self.add_standard_volume_name = QtWidgets.QPushButton(self.centralwidget)
        self.add_standard_volume_name.setGeometry(QtCore.QRect(578, 470, 161, 31))
        self.add_standard_volume_name.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                                   "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                                   "                                       color:rgb(75,0,130);\n"
                                                   "                                       font-weight: bold;")
        self.add_standard_volume_name.setObjectName("add_standard_volume_name")
        self.add_standard_volume_name.setVisible(False)
        #roi
        self.add_new_roi = QtWidgets.QPushButton(self.centralwidget)
        self.add_new_roi.setGeometry(QtCore.QRect(598, 470, 141, 31))
        self.add_new_roi.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                                    "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                                    "                                       color:rgb(75,0,130);\n"
                                                    "                                       font-weight: bold;")
        self.add_new_roi.setObjectName("add_new_roi")
        self.add_new_roi.setVisible(False)

        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(638, 554, 101, 31))
        self.cancel_button.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                         " font: 57 11pt \\\"Ubuntu\\\";\n"
                                         "\n"
                                         "font-weight: bold;\n"
                                         "color: rgb(85, 87, 83);")
        self.cancel_button.setObjectName("cancel_button")
        self.apply_button = QtWidgets.QPushButton(self.centralwidget)
        self.apply_button.setGeometry(QtCore.QRect(510, 554, 111, 31))
        self.apply_button.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                        "                                       font: 57 11pt \\\"Ubuntu\\\";\n"
                                        "                                       color:rgb(75,0,130);\n"
                                        "                                       font-weight: bold;")
        self.apply_button.setObjectName("apply_button")
        self.treeList = QtWidgets.QTreeView(self.centralwidget)
        self.treeList.setGeometry(QtCore.QRect(10, 40, 256, 461))
        self.treeList.setObjectName("treeList")
        self.treeList.setStyleSheet("QTreeView::item { padding: 10px }")
        PluginManager.setCentralWidget(self.centralwidget)
        self.treeList.setHeaderHidden(True)
        self.retranslateUi(PluginManager)
        QtCore.QMetaObject.connectSlotsByName(PluginManager)

    def retranslateUi(self, PluginManager):
        _translate = QtCore.QCoreApplication.translate
        PluginManager.setWindowTitle(_translate("PluginManager", "Plugin Manager"))
        self.optionTitle.setText(_translate("PluginManager", ""))
        self.enabled.setText(_translate("PluginManager", "Enabled"))
        self.cancel_button.setText(_translate("PluginManager", "Cancel"))
        self.apply_button.setText(_translate("PluginManager", "Apply"))
        self.add_new_window.setText(_translate("PluginManager", "Add New Window"))
        self.add_standard_organ_name.setText(_translate("PluginManager", "Add Standard Name"))
        self.add_standard_volume_name.setText(_translate("PluginManager", "Add Standard Name"))
        self.import_organ_csv.setText(_translate("PluginManager", "Import Spreadsheet"))
        self.add_new_roi.setText(_translate("PluginManager", "Add new ROI"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    PluginManager = QtWidgets.QMainWindow()
    ui = Ui_PluginManager()
    ui.setupUi(PluginManager)
    PluginManager.show()
    sys.exit(app.exec_())
