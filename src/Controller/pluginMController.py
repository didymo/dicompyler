import csv
import sys
from collections import deque

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem

from src.View.PluginManager import *
from src.data.csv import *


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
        self.fillTables()
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
            self.enabled.setVisible(True)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(True)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(True)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(True)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(True)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(True)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(True)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(True)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)
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
            self.enabled.setVisible(False)
            self.enabledHash.setVisible(False)
            self.enabledROI.setVisible(False)
            self.enabledWindow.setVisible(False)
            self.enabledOrgan.setVisible(False)
            self.enabledVolume.setVisible(False)

    def fillTables(self):
        with open('src/data/csv/imageWindowing.csv', "r") as fileInput:
            enabled = next(fileInput)
            enabled = enabled.replace(',', '')
            enabled = enabled.replace('\n','')
            if (str(enabled) == 'Enabled'):
                self.enabledWindow.setChecked(True)
            else:
                self.enabledWindow.setChecked(False)
            i=0;
            for row in fileInput:
                items = [
                    QTableWidgetItem(str(item))
                    for item in row.split(',')
                ]

                self.table_view.insertRow(i)
                self.table_view.setItem(i, 0, items[0])
                self.table_view.setItem(i, 1, items[1])
                self.table_view.setItem(i, 2, items[2])
                self.table_view.setItem(i, 3, items[3])
                i+=1

        #organ names
        with open('src/data/csv/organName.csv', "r") as fileInput:
            enabled = next(fileInput)
            enabled = enabled.replace(',', '')
            enabled = enabled.replace('\n','')
            if (enabled == 'Enabled'):
                self.enabledOrgan.setChecked(True)
            else:
                self.enabledOrgan.setChecked(False)
            i = 0;
            for row in fileInput:
                items = [
                    QTableWidgetItem(str(item.replace('\n', '')))
                    for item in row.split(',')
                ]

                self.table_organ.insertRow(i)
                self.table_organ.setItem(i, 0, items[0])
                self.table_organ.setItem(i, 1, items[1])
                self.table_organ.setItem(i, 2, items[2])
                i += 1

        #volume name
        with open('src/data/csv/volumeName.csv', "r") as fileInput:
            enabled = next(fileInput)
            enabled = enabled.replace(',', '')
            enabled = enabled.replace('\n','')
            if (enabled == 'Enabled'):
                self.enabledVolume.setChecked(True)
            else:
                self.enabledVolume.setChecked(False)
            i = 0;
            for row in fileInput:
                items = [
                    QTableWidgetItem(str(item.replace('\n', '')))
                    for item in row.split(',')
                ]
                self.table_volume.insertRow(i)
                self.table_volume.setItem(i, 0, items[0])
                self.table_volume.setItem(i, 1, items[1])
                self.table_volume.setItem(i, 2, items[2])
                i += 1

        #roi isodose
        with open('src/data/csv/isodoseRoi.csv', "r") as fileInput:
            enabled = next(fileInput)
            enabled = enabled.replace(',', '')
            enabled = enabled.replace('\n','')
            if (enabled == 'Enabled'):
                self.enabledROI.setChecked(True)
            else:
                self.enabledROI.setChecked(False)
            i = 0;
            for row in fileInput:
                items = [
                    QTableWidgetItem(str(item.replace('\n', '')))
                    for item in row.split(',')
                ]

                self.table_roi.insertRow(i)
                self.table_roi.setItem(i, 0, items[0])
                self.table_roi.setItem(i, 1, items[1])
                i += 1
        #patient hash
        with open('src/data/csv/patientHash.csv', "r") as fileInput:
            enabled = next(fileInput)
            enabled = enabled.replace(',', '')
            enabled = enabled.replace('\n','')
            if (enabled == 'Enabled'):
                self.enabledHash.setChecked(True)
            else:
                self.enabledHash.setChecked(False)
            i = 0;
            for row in fileInput:
                items = [
                    QTableWidgetItem(str(item.replace('\n', '')))
                    for item in row.split(',')
                ]

                self.table_Ids.insertRow(i)
                self.table_Ids.setItem(i, 0, items[0])
                self.table_Ids.setItem(i, 1, items[1])
                i += 1



class PManager:

    def __init__(self):
        pass

    def show_plugin_manager(self):
        self.plugin_window = PluginManager()
        self.plugin_window.show()
