import sys
from collections import deque

from PyQt5 import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QVBoxLayout, QLayout, QAbstractItemView

from src.View.PluginManager import *

class PluginManager(QtWidgets.QMainWindow, Ui_PluginManager):

    def __init__(self):
        super(PluginManager, self).__init__()
        self.setupUi(self)
        data = [
            {'level': 0, 'dbID': 77, 'parent_ID': 6, 'short_name': 'Built-In Plugins'},
            {'level': 1, 'dbID': 88, 'parent_ID': 77, 'short_name': '2D View'},
            {'level': 1, 'dbID': 89, 'parent_ID': 77, 'short_name': 'Anonymize'},
            {'level': 1, 'dbID': 90, 'parent_ID': 77, 'short_name': 'DVH'},
            {'level': 0, 'dbID': 442, 'parent_ID': 6, 'short_name': 'User Plugins'},
            {'level': 1, 'dbID': 522, 'parent_ID': 442, 'short_name': 'Image Windowing'},
            {'level': 1, 'dbID': 556, 'parent_ID': 442, 'short_name': 'Standard Organ Names'},
            {'level': 1, 'dbID': 527, 'parent_ID': 442, 'short_name': 'Standard Volume Names'},
            {'level': 1, 'dbID': 528, 'parent_ID': 442, 'short_name': 'Create ROI from Isodose'},
            {'level': 1, 'dbID': 520, 'parent_ID': 442, 'short_name': 'Patient ID - Hash ID'}
        ]
        self.model = QtGui.QStandardItemModel()
        self.treeList.setModel(self.model)
        self.importData(data)
        self.treeList.expandAll()
        self.treeList.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.cancel_button.clicked.connect(self.close)
        self.apply_button.clicked.connect(self.applyChanges)
        self.treeList.clicked.connect(self.display)


    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value['level'] == 0:
                parent = root
            else:
                pid = value['parent_ID']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            dbid = value['dbID']
            parent.appendRow([
                QtGui.QStandardItem(value['short_name'])
            ])
            seen[dbid] = parent.child(parent.rowCount() - 1)

    def applyChanges(self):
        pass

    def display(self,index):
        item = self.treeList.selectedIndexes()[0]
        self.optionTitle.setText(item.model().itemFromIndex(index).text())
        self.tableDisplay(item.model().itemFromIndex(index).text())

    def tableDisplay(self, type):
        #create a file that keeps a record of the tables and call to populate the given table
        if type == "2D View":
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "Anonymize":
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "DVH":
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "Image Windowing":
            self.table_modules.setColumnCount(4)
            self.table_modules.setHorizontalHeaderLabels([" Window Name ", " Scan ", " Upper Value ", " Lower Value "])
            self.table_modules.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignLeft)
            header = self.table_modules.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            self.add_new_window.setVisible(True)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Standard Organ Names":
            self.table_modules.setColumnCount(3)
            self.table_modules.setHorizontalHeaderLabels([" Standard Name ", " FMA ID ", " Organ "])
            self.table_modules.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
            header = self.table_modules.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(True)
            self.import_organ_csv.setVisible(True)
        elif type == "Standard Volume Names":
            self.table_modules.setColumnCount(3)
            self.table_modules.setHorizontalHeaderLabels([" Standard Name ", " FMA ID ", " Volume "])
            self.table_modules.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
            header = self.table_modules.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(True)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Create ROI from Isodose":
            self.table_modules.setColumnCount(2)
            self.table_modules.setHorizontalHeaderLabels([" Isodose Level (cGy) ", " ROI name "])
            self.table_modules.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            header = self.table_modules.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(True)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Patient ID - Hash ID":
            self.table_modules.setColumnCount(2)
            self.table_modules.setHorizontalHeaderLabels([" Patient ID ", " Hash ID "])
            self.table_modules.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            self.table_modules.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            header = self.table_modules.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Built-In Plugins" or type == "User Plugins":
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)


class PManager:

    def __init__(self):
        pass

    def show_plugin_manager(self):
        self.plugin_window = PluginManager()
        self.plugin_window.show()