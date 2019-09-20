import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pylab as plt
import numpy as np
from src.Model.LoadPatients import *
from src.Model.CalculateDVHs import *
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QCompleter, QLineEdit
from country_list import countries_for_language
from array import *
import numpy as np
import csv
from src.Model.CalculateImages import *
from src.Model.GetPatientInfo import *
from src.Controller.mainPageController import MainPage
from matplotlib.backends.backend_qt5agg import FigureCanvas



class Ui_MainWindow(object):

    def setupUi(self, MainWindow, path):
        # Load all information from the patient
        self.path = path
        self.dataset, self.filepaths = get_datasets(path)
        self.pixmaps = get_pixmaps(self.dataset)
        self.file_rtss = self.filepaths['rtss']
        self.file_rtdose = self.filepaths['rtdose']
        self.dataset_rtss = pydicom.dcmread(self.file_rtss)
        self.dataset_rtdose = pydicom.dcmread(self.file_rtdose)
        self.rois = get_roi_info(self.dataset_rtss)
        self.selected_rois = []
        self.dvh = self.getDVH()
        self.basicInfo = get_basic_info(self.dataset[0])
        self.dict_windowing = {"normal": [None, None], "lung": [2152, 52], "bone": [1401, 700], "brain": [168, 34], "soft tissue": [330, -24]}

        self.callClass = MainPage(self.path, self.dataset, self.filepaths)

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 700)

        # Central Layer
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Left Column
        self.tab1 = QtWidgets.QTabWidget(self.centralwidget)
        self.tab1.setGeometry(QtCore.QRect(0, 40, 200, 361))
        self.tab1.setObjectName("tab1")

        # Left Column: Structures tab
        self.tab1_structures = QtWidgets.QWidget()
        self.tab1_structures.setObjectName("tab1_structures")
        self.updateStructureColumn()

        # color1_struct = QtGui.QPixmap(10, 10)
        # color1_struct.fill(QtGui.QColor(255, 144, 3))
        # self.coloriconAnonymize_and_Save_struct = QtGui.QIcon(color1_struct)
        # self.colorButton_struct = QtWidgets.QToolButton()
        # self.colorButton_struct.setIcon(self.coloriconAnonymize_and_Save_struct)
        # self.frame_structures.addWidget(self.painter, 0, 0, 1, 1)
        # self.button1_struct = QtWidgets.QCheckBox("ROI1")
        # self.frame_structures.addWidget(self.button1_struct)
        # self.frame_structures.setAlignment(self.button1_struct, QtCore.Qt.AlignTop)
        self.tab1.addTab(self.tab1_structures, "")

        # Left Column: Isodoses tab
        self.tab1_isodoses = QtWidgets.QWidget()
        self.tab1_isodoses.setObjectName("tab1_isodoses")
        self.vbox_isod = QtWidgets.QVBoxLayout(self.tab1_isodoses)
        self.box1_isod = QtWidgets.QCheckBox("90 % / 6300 cGy [Max]")
        self.box2_isod = QtWidgets.QCheckBox("102 % / 7140 cGy")
        self.box3_isod = QtWidgets.QCheckBox("100 % / 7000 cGy")
        self.box4_isod = QtWidgets.QCheckBox("98 % / 6860 cGy")
        self.box5_isod = QtWidgets.QCheckBox("95 % / 6650 cGy")
        self.box6_isod = QtWidgets.QCheckBox("90 % / 6300 cGy")
        self.box7_isod = QtWidgets.QCheckBox("80 % / 5600 cGy")
        self.box8_isod = QtWidgets.QCheckBox("70 % / 4900 cGy")
        self.box9_isod = QtWidgets.QCheckBox("50 % / 3500 cGy")
        self.box10_isod = QtWidgets.QCheckBox("30 % / 2100 cGy")
        self.box1_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box2_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box3_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box4_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box5_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box6_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box7_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box8_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box9_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.box10_isod.setStyleSheet("font: 10pt \"Laksaman\";")
        self.vbox_isod.addWidget(self.box1_isod)
        self.vbox_isod.addWidget(self.box2_isod)
        self.vbox_isod.addWidget(self.box3_isod)
        self.vbox_isod.addWidget(self.box4_isod)
        self.vbox_isod.addWidget(self.box5_isod)
        self.vbox_isod.addWidget(self.box6_isod)
        self.vbox_isod.addWidget(self.box7_isod)
        self.vbox_isod.addWidget(self.box8_isod)
        self.vbox_isod.addWidget(self.box9_isod)
        self.vbox_isod.addWidget(self.box10_isod)
        self.tab1.addTab(self.tab1_isodoses, "")

        # Main view
        self.tab2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tab2.setGeometry(QtCore.QRect(200, 40, 880, 561))
        self.tab2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tab2.setObjectName("tab2")

        # Main view: DICOM View
        self.tab2_view = QtWidgets.QWidget()
        self.tab2_view.setObjectName("tab2_view")
        self.gridLayout_view = QtWidgets.QGridLayout(self.tab2_view)
        self.gridLayout_view.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_view.setHorizontalSpacing(0)

        # Vertical Slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.pixmaps) - 1)
        self.slider.setValue(int(len(self.pixmaps) / 2))
        self.slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet("QSlider::handle:vertical:hover {background: qlineargradient(x1:0, y1:0, x2:1, "
                                  "y2:1, stop:0 #fff, stop:1 #ddd);border: 1px solid #444;border-radius: 4px;}")
        # self.slider.setAutoFillBackground(True)
        # p = self.slider.palette()
        # p.setColor(self.slider.backgroundRole(), QtCore.Qt.black)
        # self.slider.setPalette(p)
        self.slider.valueChanged.connect(self.valueChangeSlider)
        self.slider.setGeometry(QtCore.QRect(0, 0, 50, 500))
        self.gridLayout_view.addWidget(self.slider, 0, 1, 1, 1)

        #DICOM image processing
        id = self.slider.value()
        DICOM_image = self.pixmaps[id]
        DICOM_image = DICOM_image.scaled(512, 512, QtCore.Qt.KeepAspectRatio)
        DICOM_image_label = QtWidgets.QLabel()
        DICOM_image_label.setPixmap(DICOM_image)
        DICOM_image_scene = QtWidgets.QGraphicsScene()
        DICOM_image_scene.addWidget(DICOM_image_label)
        # Introduce DICOM image into DICOM View tab
        self.DICOM_view = QtWidgets.QGraphicsView(self.tab2_view)
        self.DICOM_view.setScene(DICOM_image_scene)
        background_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0), QtCore.Qt.SolidPattern)
        self.DICOM_view.setBackgroundBrush(background_brush)
        self.DICOM_view.setGeometry(QtCore.QRect(0, 0, 877, 517))
        self.DICOM_view.setObjectName("DICOM_view")

        self.gridLayout_view.addWidget(self.DICOM_view, 0, 0, 1, 1)

        self.tab2.addTab(self.tab2_view, "")


        # Main view: DVH
        self.tab2_DVH = QtWidgets.QWidget()
        self.tab2_DVH.setObjectName("tab2_DVH")
        # DVH layout
        self.widget_DVH = QtWidgets.QWidget(self.tab2_DVH)
        self.widget_DVH.setGeometry(QtCore.QRect(0, 0, 877, 400))
        self.widget_DVH.setObjectName("widget_DVH")
        self.gridL_DVH = QtWidgets.QGridLayout(self.widget_DVH)
        self.gridL_DVH.setObjectName("gridL_DVH")

        # DVH Processing
        self.initDVH_view()

        # DVH: Export DVH Button
        self.vbox_DVH = QtWidgets.QVBoxLayout()
        self.button_exportDVH = QtWidgets.QPushButton()
        self.button_exportDVH.setFixedSize(QtCore.QSize(100, 39))
        self.button_exportDVH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportDVH.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                       "font: 57 11pt \"Ubuntu\";\n"
                                       "color:rgb(75,0,130);\n"
                                       "font-weight: bold;\n")
        self.button_exportDVH.setObjectName("button_exportDVH")

        # self.spacer = QtWidgets.QWidget()
        # self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.vbox_DVH.addWidget(self.spacer)
        self.vbox_DVH.addWidget(self.button_exportDVH)

        # self.vbox_DVH.setAlignment(self.button_exportDVH, QtCore.Qt.AlignBottom)
        # self.vbox_DVH.addStretch(30)
        self.gridL_DVH.addLayout(self.vbox_DVH, 1, 1, 1, 1)

        self.tab2.addTab(self.tab2_DVH, "")


        # Main view: DICOM Tree
        self.tab2_DICOM_tree = QtWidgets.QWidget()
        self.tab2_DICOM_tree.setObjectName("tab2_DICOM_tree")
        # Tree View tab grid layout
        self.vboxL_Tree = QtWidgets.QVBoxLayout(self.tab2_DICOM_tree)
        self.vboxL_Tree.setObjectName("vboxL_Tree")
        self.vboxL_Tree.setContentsMargins(0, 0, 0, 0)
        # Tree view selector
        self.comboBox_TreeSelector = QtWidgets.QComboBox()
        self.comboBox_TreeSelector.setStyleSheet("font: 75 10pt \"Laksaman\";")
        self.comboBox_TreeSelector.addItem("Select...")
        self.comboBox_TreeSelector.setGeometry(QtCore.QRect(5, 35, 188, 31))
        self.vboxL_Tree.addWidget(self.comboBox_TreeSelector)
        # Creation of the Tree View
        self.treeView = QtWidgets.QTreeView(self.tab2_DICOM_tree)
        self.initTree()
        self.updateTree(self.slider.value())
        # Set parameters for the Tree View
        self.treeView.header().resizeSection(0, 280)
        self.treeView.header().resizeSection(1, 380)
        self.treeView.header().resizeSection(2, 100)
        self.treeView.header().resizeSection(3, 50)
        self.treeView.header().resizeSection(4, 50)
        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setGeometry(QtCore.QRect(0, 0, 877, 517))
        self.treeView.expandAll()
        self.treeView.setObjectName("treeView")
        self.vboxL_Tree.addWidget(self.treeView)
        self.tab2.addTab(self.tab2_DICOM_tree, "")

        # Main view: Clinical Data
        self.tab2_clinical_data = QtWidgets.QWidget()
        # check for csv data
        reg = '/[clinicaldata]*[.csv]'
        if not glob.glob(self.path + reg):
            self.callClass.display_cd_form(self.tab2,self.path)
        else:
            self.callClass.display_cd_dat(self.tab2,self.path)

        # Bottom Layer
        self.frame_bottom = QtWidgets.QFrame(self.centralwidget)
        self.frame_bottom.setGeometry(QtCore.QRect(0, 600, 1080, 27))
        self.frame_bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom.setObjectName("frame_bottom")

        # Bottom Layer: "@Onko2019" label
        self.label = QtWidgets.QLabel(self.frame_bottom)
        self.label.setGeometry(QtCore.QRect(1000, 0, 91, 29))
        self.label.setStyleSheet("font: 9pt \"Laksaman\";")
        self.label.setObjectName("label")

        # Left Column: Structure Information
        self.frame_struct_info = QtWidgets.QFrame(self.centralwidget)
        self.frame_struct_info.setGeometry(QtCore.QRect(0, 400, 200, 201))
        self.frame_struct_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_struct_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_struct_info.setObjectName("frame_struct_info")

        # Structure Information: "Select Structure" combobox
        self.comboBox = QtWidgets.QComboBox(self.frame_struct_info)
        self.comboBox.setStyleSheet("font: 75 10pt \"Laksaman\";")
        self.comboBox.addItem("Select...")
        for key, value in self.rois.items():
            self.comboBox.addItem(value['name'])
        self.comboBox.setGeometry(QtCore.QRect(5, 35, 188, 31))
        self.comboBox.setObjectName("comboBox")

        # Structure Information: "Volume" label
        self.struct_volume_label = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_volume_label.setGeometry(QtCore.QRect(10, 70, 68, 29))
        self.struct_volume_label.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_volume_label.setObjectName("struct_volume_label")

        # Structure Information: "Min Dose" label
        self.struct_minDose_label = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_minDose_label.setGeometry(QtCore.QRect(10, 100, 68, 31))
        self.struct_minDose_label.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_minDose_label.setObjectName("struct_minDose_label")

        # Structure Information: "Max Dose" label
        self.struct_maxDose_label = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_maxDose_label.setGeometry(QtCore.QRect(10, 130, 68, 31))
        self.struct_maxDose_label.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_maxDose_label.setObjectName("struct_maxDose_label")

        # Structure Information: "Mean Dose" label
        self.struct_meanDose_label = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_meanDose_label.setGeometry(QtCore.QRect(10, 160, 81, 31))
        self.struct_meanDose_label.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_meanDose_label.setObjectName("struct_meanDose_label")

        # Structure Information: "Volume" box
        self.struct_volume_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_volume_box.setGeometry(QtCore.QRect(90, 70, 81, 31))
        self.struct_volume_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_volume_box.setObjectName("struct_volume_box")

        # Structure Information: "Min Dose" box
        self.struct_minDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_minDose_box.setGeometry(QtCore.QRect(90, 100, 81, 31))
        self.struct_minDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_minDose_box.setObjectName("struct_minDose_box")

        # Structure Information: "Max Dose" box
        self.struct_maxDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_maxDose_box.setGeometry(QtCore.QRect(90, 130, 81, 31))
        self.struct_maxDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_maxDose_box.setObjectName("struct_maxDose_box")

        # Structure Information: "Mean Dose" box
        self.struct_meanDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_meanDose_box.setGeometry(QtCore.QRect(90, 160, 81, 31))
        self.struct_meanDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_meanDose_box.setObjectName("struct_meanDose_box")

        # Layout Icon and Text "Structure Information"
        self.widget = QtWidgets.QWidget(self.frame_struct_info)
        self.widget.setGeometry(QtCore.QRect(5, 5, 160, 28))
        self.widget.setObjectName("widget")
        self.gridL_StructInfo = QtWidgets.QGridLayout(self.widget)
        self.gridL_StructInfo.setContentsMargins(0, 0, 0, 0)
        self.gridL_StructInfo.setObjectName("gridL_StructInfo")

        # Structure Information: Information Icon
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/images/Icon/info.png"))
        self.label_3.setObjectName("label_3")
        self.gridL_StructInfo.addWidget(self.label_3, 1, 0, 1, 1)

        # Structure Information: Structure Information Label
        self.struct_info_label = QtWidgets.QLabel(self.widget)
        self.struct_info_label.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.struct_info_label.setObjectName("struct_info_label")
        self.gridL_StructInfo.addWidget(self.struct_info_label, 1, 1, 1, 1)

        self.label_3.raise_()
        self.struct_info_label.raise_()
        self.comboBox.raise_()
        self.struct_volume_label.raise_()
        self.struct_minDose_label.raise_()
        self.struct_maxDose_label.raise_()
        self.struct_meanDose_label.raise_()
        self.struct_volume_box.raise_()
        self.struct_minDose_box.raise_()
        self.struct_maxDose_box.raise_()
        self.struct_meanDose_box.raise_()

        # Patient Bar

        # Patient Icon
        self.patient_icon = QtWidgets.QLabel(self.centralwidget)
        self.patient_icon.setGeometry(QtCore.QRect(10, 5, 30, 30))
        self.patient_icon.setText("")
        self.patient_icon.setPixmap(QtGui.QPixmap(":/images/Icon/patient.png"))
        self.patient_icon.setObjectName("patient_icon")

        # Name Patient (layout)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(50, 5, 370, 31))
        self.widget3.setObjectName("widget3")
        self.gridLayout_name = QtWidgets.QGridLayout(self.widget3)
        self.gridLayout_name.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_name.setObjectName("gridLayout_name")

        # Name Patient (label)
        self.patient_name = QtWidgets.QLabel(self.widget3)
        self.patient_name.setObjectName("patient_name")
        self.patient_name.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.gridLayout_name.addWidget(self.patient_name, 0, 0, 1, 1)

        # Name Patient (box)
        self.patient_name_box = QtWidgets.QLabel(self.widget3)
        self.patient_name_box.setObjectName("patient_name_box")
        self.patient_name_box.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.patient_name_box.setFont(QtGui.QFont("Laksaman", pointSize=10))
        self.gridLayout_name.addWidget(self.patient_name_box, 0, 1, 1, 1)

        # Patient ID (layout)
        self.widget4 = QtWidgets.QWidget(self.centralwidget)
        self.widget4.setGeometry(QtCore.QRect(500, 5, 280, 31))
        self.widget4.setObjectName("widget4")
        self.gridLayout_ID = QtWidgets.QGridLayout(self.widget4)
        self.gridLayout_ID.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_ID.setObjectName("gridLayout_ID")

        # Patient ID (label)
        self.patient_ID = QtWidgets.QLabel(self.widget4)
        self.patient_ID.setObjectName("patient_ID")
        self.patient_ID.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.gridLayout_ID.addWidget(self.patient_ID, 0, 0, 1, 1)

        # Patient ID (box)
        self.patient_ID_box = QtWidgets.QLabel(self.widget4)
        self.patient_ID_box.setObjectName("patient_ID_box")
        self.patient_ID_box.setFont(QtGui.QFont("Laksaman", pointSize=10))
        self.gridLayout_ID.addWidget(self.patient_ID_box, 0, 1, 1, 1)

        # Gender (layout)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(830, 5, 111, 31))
        self.widget2.setObjectName("widget2")
        self.gridLayout_gender = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_gender.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_gender.setObjectName("gridLayout_gender")

        # Gender (label)
        self.patient_gender = QtWidgets.QLabel(self.widget2)
        self.patient_gender.setObjectName("patient_gender")
        self.patient_gender.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.gridLayout_gender.addWidget(self.patient_gender, 0, 0, 1, 1)

        # Gender (box)
        self.patient_gender_box = QtWidgets.QLabel(self.widget2)
        self.patient_gender_box.setObjectName("patient_gender_box")
        self.patient_gender_box.setFont(QtGui.QFont("Laksaman", pointSize=10))
        self.gridLayout_gender.addWidget(self.patient_gender_box, 0, 1, 1, 1)

        # Date of Birth (layout)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(950, 5, 95, 31))
        self.widget1.setObjectName("widget1")
        self.gridLayout_DOB = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_DOB.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_DOB.setObjectName("gridLayout_DOB")

        # Date of Birth (label)
        self.patient_DOB = QtWidgets.QLabel(self.widget1)
        self.patient_DOB.setObjectName("patient_DOB")
        self.patient_DOB.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.gridLayout_DOB.addWidget(self.patient_DOB, 0, 0, 1, 1)

        # Date of Birth (box)
        self.patient_DOB_box = QtWidgets.QLabel(self.widget1)
        self.patient_DOB_box.setObjectName("patient_DOB_box")
        self.patient_DOB_box.setFont(QtGui.QFont("Laksaman", pointSize=10))
        self.gridLayout_DOB.addWidget(self.patient_DOB_box, 0, 1, 1, 1)

        self.patient_icon.raise_()
        self.patient_name.raise_()
        self.patient_name_box.raise_()
        self.patient_ID.raise_()
        self.patient_ID_box.raise_()
        self.patient_gender_box.raise_()
        self.patient_DOB_box.raise_()
        self.patient_gender.raise_()
        self.patient_DOB.raise_()
        self.patient_gender_box.raise_()
        self.patient_gender.raise_()
        self.patient_DOB_box.raise_()
        self.patient_gender_box.raise_()
        self.tab1.raise_()
        self.tab2.raise_()
        self.frame_bottom.raise_()
        self.frame_struct_info.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 901, 35))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Menu Bar: File, Edit, Tools, Help
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")


        # All icons used for menu bar and toolbar
        iconOpen = QtGui.QIcon()
        iconOpen.addPixmap(QtGui.QPixmap(":/images/Icon/open_patient.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconAnonymize_and_Save = QtGui.QIcon()
        iconAnonymize_and_Save.addPixmap(QtGui.QPixmap(":/images/Icon/save_all.png"),
                                         QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconZoom_In = QtGui.QIcon()
        iconZoom_In.addPixmap(QtGui.QPixmap(":/images/Icon/plus.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconZoom_Out = QtGui.QIcon()
        iconZoom_Out.addPixmap(QtGui.QPixmap(":/images/Icon/minus.png"),
                               QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconWindowing = QtGui.QIcon()
        iconWindowing.addPixmap(QtGui.QPixmap(":/images/Icon/windowing.png"),
                                QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconTransect = QtGui.QIcon()
        iconTransect.addPixmap(QtGui.QPixmap(":/images/Icon/transect.png"),
                               QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconBrush = QtGui.QIcon()
        iconBrush.addPixmap(QtGui.QPixmap(":/images/Icon/ROI_Brush.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconIsodose = QtGui.QIcon()
        iconIsodose.addPixmap(QtGui.QPixmap(":/images/Icon/ROI_Isodose.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconPlugin_Manager = QtGui.QIcon()
        iconPlugin_Manager.addPixmap(QtGui.QPixmap(":/images/Icon/management.png"),
                                     QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconExport = QtGui.QIcon()
        iconExport.addPixmap(QtGui.QPixmap(":/images/Icon/export.png"),
                             QtGui.QIcon.Normal, QtGui.QIcon.On)


        # Set Menu Bar (Tools tab)
        self.menuWindowing = QtWidgets.QMenu(self.menuTools)
        self.menuWindowing.setObjectName("menuWindowing")
        self.menuWindowing.setIcon(iconWindowing)
        self.menuROI_Creation = QtWidgets.QMenu(self.menuTools)
        self.menuROI_Creation.setObjectName("menuROI_Creation")
        self.menuExport = QtWidgets.QMenu(self.menuTools)
        self.menuExport.setIcon(iconExport)
        self.menuExport.setObjectName("menuExport")

        # Set Tool Bar
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)


        # Open Patient Action
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setIcon(iconOpen)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")

        # Import Action
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")

        # Save Action
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        # Save as Anonymous Action
        self.actionSave_as_Anonymous = QtWidgets.QAction(MainWindow)
        self.actionSave_as_Anonymous.setObjectName("actionSave_as_Anonymous")

        # Exit Action
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        # Undo Action
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")

        # Redo Action
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")

        # Rename ROI Action
        self.actionRename_ROI = QtWidgets.QAction(MainWindow)
        self.actionRename_ROI.setObjectName("actionRename_ROI")

        # Delete ROI Action
        self.actionDelete_ROI = QtWidgets.QAction(MainWindow)
        self.actionDelete_ROI.setObjectName("actionDelete_ROI")

        # Zoom In Action
        self.actionZoom_In = QtWidgets.QAction(MainWindow)
        self.actionZoom_In.setIcon(iconZoom_In)
        self.actionZoom_In.setIconVisibleInMenu(True)
        self.actionZoom_In.setObjectName("actionZoom_In")

        # Zoom Out Action
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)

        self.actionZoom_Out.setIcon(iconZoom_Out)
        self.actionZoom_Out.setIconVisibleInMenu(True)
        self.actionZoom_Out.setObjectName("actionZoom_Out")

        # Windowing Action
        self.actionWindowing = QtWidgets.QAction(MainWindow)
        self.actionWindowing.setIcon(iconWindowing)
        self.actionWindowing.setIconVisibleInMenu(True)
        self.actionWindowing.setObjectName("actionWindowing")
        self.initWindowingMenu(MainWindow)
        # self.actionWindowingNormal = QtWidgets.QAction(MainWindow)
        # self.actionWindowingNormal.setObjectName("actionWindowingNormal")
        # self.actionWindowingLung = QtWidgets.QAction(MainWindow)
        # self.actionWindowingLung.setObjectName("actionWindowingLung")
        # self.actionWindowingBone = QtWidgets.QAction(MainWindow)
        # self.actionWindowingBone.setObjectName("actionWindowingBone")
        # self.actionWindowingSoftTissue = QtWidgets.QAction(MainWindow)
        # self.actionWindowingSoftTissue.setObjectName("actionWindowingSoftTissue")
        # self.actionWindowingBrain = QtWidgets.QAction(MainWindow)
        # self.actionWindowingBrain.setObjectName("actionWindowingBrain")
        # self.actionWindowingHeadNeck = QtWidgets.QAction(MainWindow)
        # self.actionWindowingHeadNeck.setObjectName("actionWindowingHeadNeck")

        # Transect Action
        self.actionTransect = QtWidgets.QAction(MainWindow)
        self.actionTransect.setIcon(iconTransect)
        self.actionTransect.setIconVisibleInMenu(True)
        self.actionTransect.setObjectName("actionTransect")

        # ROI by brush Action
        self.actionBrush = QtWidgets.QAction(MainWindow)
        self.actionBrush.setIcon(iconBrush)
        self.actionBrush.setIconVisibleInMenu(True)
        self.actionBrush.setObjectName("actionBrush")

        # ROI by Isodose Action
        self.actionIsodose = QtWidgets.QAction(MainWindow)
        self.actionIsodose.setIcon(iconIsodose)
        self.actionIsodose.setIconVisibleInMenu(True)
        self.actionIsodose.setObjectName("actionIsodose")

        # Plugin Manager Action
        self.actionPlugin_Manager = QtWidgets.QAction(MainWindow)
        self.actionPlugin_Manager.setIcon(iconPlugin_Manager)
        self.actionPlugin_Manager.setIconVisibleInMenu(True)
        self.actionPlugin_Manager.setObjectName("actionPlugin_Manager")

        # Anonymize and Save Action
        self.actionAnonymize_and_Save = QtWidgets.QAction(MainWindow)
        self.actionAnonymize_and_Save.setIcon(iconAnonymize_and_Save)
        self.actionAnonymize_and_Save.setIconVisibleInMenu(True)
        self.actionAnonymize_and_Save.setObjectName("actionAnonymize_and_Save")
        self.actionAnonymize_and_Save.triggered.connect(self.HandleAnonymization)


        # Export DVH Spreadsheet Action
        self.actionDVH_Spreadsheet = QtWidgets.QAction(MainWindow)
        self.actionDVH_Spreadsheet.setObjectName("actionDVH_Spreadsheet")

        # Export Clinical Data Action
        self.actionClinical_Data = QtWidgets.QAction(MainWindow)
        self.actionClinical_Data.setObjectName("actionClinical_Data")

        # Export Pyradiomics Action
        self.actionPyradiomics = QtWidgets.QAction(MainWindow)
        self.actionPyradiomics.setObjectName("actionPyradiomics")
        self.actionPyradiomics.triggered.connect(self.pyradiomicsHandler)


        # Build menu bar
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as_Anonymous)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionRename_ROI)
        self.menuEdit.addAction(self.actionDelete_ROI)
        # self.menuWindowing.addAction(self.actionWindowingNormal)
        # self.menuWindowing.addAction(self.actionWindowingBone)
        # self.menuWindowing.addAction(self.actionWindowingBrain)
        # self.menuWindowing.addAction(self.actionWindowingHeadNeck)
        # self.menuWindowing.addAction(self.actionWindowingLung)
        # self.menuWindowing.addAction(self.actionWindowingSoftTissue)
        self.menuROI_Creation.addAction(self.actionBrush)
        self.menuROI_Creation.addAction(self.actionIsodose)
        self.menuExport.addAction(self.actionDVH_Spreadsheet)
        self.menuExport.addAction(self.actionClinical_Data)
        self.menuExport.addAction(self.actionPyradiomics)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # Windowing drop-down list on toolbar
        self.windowingButton = QtWidgets.QToolButton()
        self.windowingButton.setMenu(self.menuWindowing)
        self.windowingButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.windowingButton.setIcon(iconWindowing)

        # Export Button drop-down list on toolbar
        self.exportButton = QtWidgets.QToolButton()
        self.exportButton.setMenu(self.menuExport)
        self.exportButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.exportButton.setIcon(iconExport)

        # Build toolbar
        self.menuTools.addAction(self.actionZoom_In)
        self.menuTools.addAction(self.actionZoom_Out)
        self.menuTools.addAction(self.menuWindowing.menuAction())
        self.menuTools.addAction(self.actionTransect)
        self.menuTools.addAction(self.menuROI_Creation.menuAction())
        self.menuTools.addAction(self.actionPlugin_Manager)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.menuExport.menuAction())
        self.menuTools.addAction(self.actionAnonymize_and_Save)

        # To create a space in the toolbar
        self.toolbar_spacer = QtWidgets.QWidget()
        self.toolbar_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # To create a space in the toolbar
        self.right_spacer = QtWidgets.QWidget()
        self.right_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_In)
        self.toolBar.addAction(self.actionZoom_Out)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.windowingButton)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTransect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionBrush)
        self.toolBar.addAction(self.actionIsodose)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlugin_Manager)
        self.toolBar.addWidget(self.toolbar_spacer)
        self.toolBar.addWidget(self.exportButton)
        self.toolBar.addAction(self.actionAnonymize_and_Save)
        # self.toolBar.addWidget(self.right_spacer)

        self.retranslateUi(MainWindow)
        self.tab1.setCurrentIndex(0)
        self.tab2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # Window title
        MainWindow.setWindowTitle(_translate("MainWindow", "Onko"))

        # Set tab labels
        self.tab1.setTabText(self.tab1.indexOf(self.tab1_structures), _translate("MainWindow", "Structures"))
        self.tab1.setTabText(self.tab1.indexOf(self.tab1_isodoses), _translate("MainWindow", "Isodoses"))
        self.tab2.setTabText(self.tab2.indexOf(self.tab2_view), _translate("MainWindow", "DICOM View"))
        self.tab2.setTabText(self.tab2.indexOf(self.tab2_DVH), _translate("MainWindow", "DVH"))
        self.tab2.setTabText(self.tab2.indexOf(self.tab2_DICOM_tree), _translate("MainWindow", "DICOM Tree"))
        self.tab2.setTabText(3, "Clinical Data")


       # self.tab2.setTabText(self.tab2.indexOf(self.tab2_clinical_data), _translate("MainWindow", "Clinical Data"))

        # Set "export DVH" button label
        self.button_exportDVH.setText(_translate("MainWindow", "Export DVH"))

        # Set bottom layer label
        self.label.setText(_translate("MainWindow", "@Onko 2019"))

        # Set structure information labels
        self.struct_volume_label.setText(_translate("MainWindow", "Volume"))
        self.struct_minDose_label.setText(_translate("MainWindow", "Min Dose"))
        self.struct_maxDose_label.setText(_translate("MainWindow", "Max Dose"))
        self.struct_meanDose_label.setText(_translate("MainWindow", "Mean Dose"))
        self.struct_info_label.setText(_translate("MainWindow", "Structure Information"))

        # Set structure information boxes
        self.struct_volume_box.setText(_translate("MainWindow", "123465"))
        self.struct_minDose_box.setText(_translate("MainWindow", "796542"))
        self.struct_maxDose_box.setText(_translate("MainWindow", "889542"))
        self.struct_meanDose_box.setText(_translate("MainWindow", "816857"))

        # Set patient bar labels
        self.patient_DOB.setText(_translate("MainWindow", "DOB"))
        self.patient_gender.setText(_translate("MainWindow", "Gender"))
        self.patient_name.setText(_translate("MainWindow", "Name"))
        self.patient_ID.setText(_translate("MainWindow", "ID"))

        # Set patient bar boxes
        self.patient_DOB_box.setText(_translate("MainWindow", self.basicInfo['dob']))
        self.patient_gender_box.setText(_translate("MainWindow", self.basicInfo['gender']))
        self.patient_ID_box.setText(_translate("MainWindow", self.basicInfo['id']))
        self.patient_name_box.setText(_translate("MainWindow", self.basicInfo['name']))

        # Set menu labels
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuWindowing.setTitle(_translate("MainWindow", "Windowing"))
        self.menuROI_Creation.setTitle(_translate("MainWindow", "ROI Creation"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

        # Set action labels (menu and tool bars)
        self.actionOpen.setText(_translate("MainWindow", "Open Patient..."))
        self.actionImport.setText(_translate("MainWindow", "Import..."))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as_Anonymous.setText(_translate("MainWindow", "Save as Anonymous..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRename_ROI.setText(_translate("MainWindow", "Rename ROI..."))
        self.actionDelete_ROI.setText(_translate("MainWindow", "Delete ROI..."))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_Out.setText(_translate("MainWindow", "Zoom Out"))
        self.actionWindowing.setText(_translate("MainWindow", "Windowing"))
        # self.actionWindowingNormal.setText(_translate("MainWindow", "Normal"))
        # self.actionWindowingLung.setText(_translate("MainWindow", "Lung"))
        # self.actionWindowingBone.setText(_translate("MainWindow", "Bone"))
        # self.actionWindowingSoftTissue.setText(_translate("MainWindow", "Soft Tissue"))
        # self.actionWindowingBrain.setText(_translate("MainWindow", "Brain"))
        # self.actionWindowingHeadNeck.setText(_translate("MainWindow", "Head and Neck"))
        self.actionTransect.setText(_translate("MainWindow", "Transect"))
        self.actionBrush.setText(_translate("MainWindow", "ROI by Brush"))
        self.actionIsodose.setText(_translate("MainWindow", "ROI by Isodose"))
        self.actionPlugin_Manager.setText(_translate("MainWindow", "Plugin Manager..."))
        self.actionAnonymize_and_Save.setText(_translate("MainWindow", "Anonymize and Save"))
        self.actionDVH_Spreadsheet.setText(_translate("MainWindow", "DVH"))
        self.actionClinical_Data.setText(_translate("MainWindow", "Clinical Data"))
        self.actionPyradiomics.setText(_translate("MainWindow", "Pyradiomics"))

        MainWindow.update()


    def updateStructureColumn(self):

        self.scrollAreaStruct = QtWidgets.QScrollArea(self.tab1_structures)
        self.scrollAreaStruct.setWidgetResizable(True)
        self.scrollAreaStruct.setGeometry(QtCore.QRect(0, 0, 200, 333))

        # self.scrollAreaStruct = QtWidgets.QScrollArea(self.tab1_structures)
        # self.scrollAreaStruct.setWidgetResizable(False)
        self.scrollAreaStruct.setGeometry(QtCore.QRect(0, 0, 198, 333))
        # self.scrollAreaStruct.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scrollAreaStruct.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.scrollContentsStruct = QtWidgets.QWidget()
        # self.scrollContentsStruct.setGeometry(QtCore.QRect(0, 0, 200, 633))
        # self.scrollContentsStruct.setObjectName("scrollContentsStruct")
        # self.scrollAreaStruct.ensureWidgetVisible(self.scrollContentsStruct)

        self.frame_structures = QtWidgets.QFrame(self.scrollAreaStruct)
        self.frame_structures.setLayout(QtWidgets.QVBoxLayout())
        self.scrollAreaStruct.setWidget(self.frame_structures)
        self.frame_structures.layout().setContentsMargins(0, 0, 0, 0)

        for key, value in self.rois.items():
            text = value['name']
            checkBoxStruct = QtWidgets.QCheckBox()
            checkBoxStruct.clicked.connect(
                lambda state, text=key: self.check(state, text))
            checkBoxStruct.setStyleSheet("font: 10pt \"Laksaman\";")
            checkBoxStruct.setText(text)
            checkBoxStruct.setObjectName(text)
            self.frame_structures.layout().addWidget(checkBoxStruct)

        # text="text"
        # boxTest = QtWidgets.QCheckBox()
        # boxTest.clicked.connect(
        #     lambda ch, text=text: print(self.selected_rois))
        # boxTest.setStyleSheet("font: 10pt \"Laksaman\";")
        # boxTest.setText("Test")
        # boxTest.setObjectName("Test")
        # self.frame_structures.layout().addWidget(boxTest)


    def check(self, state, text):
        if state:
            self.selected_rois.append(text)
        else:
            self.selected_rois.remove(text)
        self.updateDVH_view()

    # In the Model directory
    def getDVH(self):
        res = dict()
        tmp = calc_dvhs(self.dataset_rtss, self.dataset_rtdose, self.rois)
        for key, value in tmp.items():
            key_int = int(key)
            res[key_int] = value
        return res


    # In the View directory
    def DVH_view(self):
        fig, ax = plt.subplots()
        fig.subplots_adjust(0.1, 0.15, 1, 1)
        max_xlim = 0
        for roi in self.selected_rois:
            dvh = self.dvh[int(roi)]
            if dvh.volume != 0:
                ax.plot(dvh.bincenters, 100 * dvh.counts / dvh.volume, label=dvh.name,
                        color=None if not isinstance(dvh.color, np.ndarray) else
                        (dvh.color / 255))
                if dvh.bincenters[-1] > max_xlim:
                    max_xlim = dvh.bincenters[-1]
                plt.xlabel('Dose [%s]' % dvh.dose_units)
                plt.ylabel('Volume [%s]' % '%')
                if dvh.name:
                    plt.legend(loc='best')
                    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        ax.set_ylim([0, 105])
        ax.set_xlim([0, max_xlim + 3])

        # Major ticks every 20, minor ticks every 5
        major_ticks_y = np.arange(0, 105, 20)
        minor_ticks_y = np.arange(0, 105, 5)
        major_ticks_x = np.arange(0, max_xlim + 3, 20)
        minor_ticks_x = np.arange(0, max_xlim + 3, 5)

        ax.set_xticks(major_ticks_x)
        ax.set_xticks(minor_ticks_x, minor=True)
        ax.set_yticks(major_ticks_y)
        ax.set_yticks(minor_ticks_y, minor=True)

        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        return fig

    def initDVH_view(self):
        fig = self.DVH_view()
        self.plotWidget = FigureCanvas(fig)
        self.gridL_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)


    def updateDVH_view(self):
        self.gridL_DVH.removeWidget(self.plotWidget)
        fig = self.DVH_view()
        self.plotWidget = FigureCanvas(fig)
        self.gridL_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)


    # When the value of the slider in the DICOM View changes
    def valueChangeSlider(self):
        id = self.slider.value()
        pixmap = self.pixmaps[id]
        pixmap = pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio)
        DICOM_image_label = QtWidgets.QLabel()
        DICOM_image_label.setPixmap(pixmap)
        DICOM_image_scene = QtWidgets.QGraphicsScene()
        DICOM_image_scene.addWidget(DICOM_image_label)
        self.DICOM_view.setScene(DICOM_image_scene)
        pass


    def initTree(self):
        self.modelTree = QtGui.QStandardItemModel(0, 5)
        self.modelTree.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
        self.modelTree.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
        self.modelTree.setHeaderData(2, QtCore.Qt.Horizontal, "Tag")
        self.modelTree.setHeaderData(3, QtCore.Qt.Horizontal, "VM")
        self.modelTree.setHeaderData(4, QtCore.Qt.Horizontal, "VR")

    def updateTree(self, id):
        filename = self.filepaths[id]
        self.dicomTree = DicomTree(filename)
        ds = self.dicomTree.read_dcm(filename)
        dict = self.dicomTree.dataset_to_dict(ds)
        parentItem = self.modelTree.invisibleRootItem()
        self.recurseBuildModel(dict, parentItem)
        self.treeView.setModel(self.modelTree)


    def recurseBuildModel(self, dict, parent):
        # For every key in the dictionary
        for key in dict:
            # The value of current key
            value = dict[key]
            # If the value is a dictionary
            if isinstance(value, type(dict)):
                # Recurse until leaf
                itemChild = QtGui.QStandardItem(key)
                parent.appendRow(self.recurseBuildModel(value, itemChild))
            else:
                # If the value is a simple item
                # Append it.
                item = [QtGui.QStandardItem(key),
                        QtGui.QStandardItem(str(value[0])),
                        QtGui.QStandardItem(str(value[1])),
                        QtGui.QStandardItem(str(value[2])),
                        QtGui.QStandardItem(str(value[3]))]
                parent.appendRow(item)
        return parent

    def initWindowingMenu(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        for key, value in self.dict_windowing.items():
            text = str(key)
            actionWindowingItem = QtWidgets.QAction(MainWindow)
            self.menuWindowing.addAction(actionWindowingItem)
            actionWindowingItem.setText(_translate("MainWindow", text))


    def pyradiomicsHandler(self):
        self.callClass.runPyradiomics()

    def HandleAnonymization(self):
        self.callClass.runAnonymization()

import src.View.resources_rc



# For Testing
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, path='dicom_sample')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())