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
        

class PManager:

    def __init__(self):
        pass

    def show_plugin_manager(self):
        self.plugin_window = PluginManager()
        self.plugin_window.show()