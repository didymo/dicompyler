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

    def display(self, index):
        item = self.treeList.selectedIndexes()[0]
        self.optionTitle.setText(item.model().itemFromIndex(index).text())
        self.changeDislpay(item.model().itemFromIndex(index).text())

    def changeDislpay(self, type):
        # create a file that keeps a record of the tables and call to populate the given table
        if type == "2D View":
            self.table_modules.setVisible(True)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "Anonymize":
            self.table_modules.setVisible(True)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "DVH":
            self.table_modules.setVisible(True)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setColumnCount(0)
        elif type == "Image Windowing":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(True)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(True)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Standard Organ Names":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(True)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(True)
            self.import_organ_csv.setVisible(True)
        elif type == "Standard Volume Names":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(True)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(True)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Create ROI from Isodose":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(True)
            self.table_Ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.add_new_roi.setVisible(True)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
        elif type == "Patient ID - Hash ID":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(True)
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
            self.table_modules.setVisible(True)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_Ids.setVisible(False)


class PManager:

    def __init__(self):
        pass

    def show_plugin_manager(self):
        self.plugin_window = PluginManager()
        self.plugin_window.show()
