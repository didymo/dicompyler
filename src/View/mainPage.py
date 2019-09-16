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
        self.dataset = get_datasets(path)
        self.pixmaps = get_pixmaps(self.dataset)
        self.file_rtss = path + "/rtss.dcm"
        self.file_rtdose = path + "/rtdose.dcm"
        self.dataset_rtss = pydicom.dcmread(self.file_rtss)
        self.dataset_rtdose = pydicom.dcmread(self.file_rtdose)
        self.rois = get_roi_info(self.dataset_rtss)
        self.selected_rois = []
        self.basicInfo = get_basic_info(self.dataset[0])
        self.callClass = MainPage(path)


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
        # self.listView = QtWidgets.QListView(self.tab1_isodoses)
        # self.listView.setGeometry(QtCore.QRect(0, 0, 200, 361))
        # self.listView.setObjectName("listView")
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
        self.hbox_DVH = QtWidgets.QHBoxLayout(self.widget_DVH)
        self.hbox_DVH.setObjectName("hbox_DVH")

        # # DVH Processing
        # DVH_file = self.getDVH()
        # fig = self.DVH_view(DVH_file)
        # self.plotWidget = FigureCanvas(fig)
        # self.hbox_DVH.addWidget(self.plotWidget)

        # DVH: Export DVH Button
        self.vbox_DVH = QtWidgets.QVBoxLayout()
        self.button_exportDVH = QtWidgets.QPushButton()
        self.button_exportDVH.setFixedSize(QtCore.QSize(100, 39))
        self.button_exportDVH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportDVH.setStyleSheet("background-color: rgb(147, 112, 219);\n""color: rgb(255, 255, 255);")
        self.button_exportDVH.setObjectName("button_exportDVH")

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.vbox_DVH.addWidget(self.spacer)
        self.vbox_DVH.addWidget(self.button_exportDVH)
        # self.vbox_DVH.setAlignment(self.button_exportDVH, QtCore.Qt.AlignBottom)
        # self.vbox_DVH.addStretch(30)
        self.hbox_DVH.addLayout(self.vbox_DVH)

        self.tab2.addTab(self.tab2_DVH, "")


        # Main view: DICOM Tree
        self.NAME, self.VALUE, self.TAG, self.VM, self.VR = range(5)
        self.tab2_DICOM_tree = QtWidgets.QWidget()
        self.tab2_DICOM_tree.setObjectName("tab2_DICOM_tree")
        # Creation of the Tree View
        self.treeView = QtWidgets.QTreeView(self.tab2_DICOM_tree)
        self.createTreeModel()
        self.updateTreeModel(self.slider.value())
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
        self.tab2.addTab(self.tab2_DICOM_tree, "")

        # Main view: Clinical Data
        self.tab2_clinical_data = QtWidgets.QWidget()
        self.tab2_clinical_data.setObjectName("tab2_clinical_data")

        #get the data that we want for the completers
        countries = dict(countries_for_language('en'))
        data = []
        for i, v in enumerate(countries):
            data.append(countries[v])
        with open('src/data/ICD10_Topography.csv', 'r') as f:
            reader = csv.reader(f)
            icd = list(reader)
            icd.pop(0)
        with open('src/data/ICD10_Topography_C.csv', 'r') as f:
            reader = csv.reader(f)
            icdc = list(reader)
        with open('src/data/ICD10_Morphology.csv', 'r') as f:
            reader = csv.reader(f)
            hist = list(reader)
            hist.pop(0)
        new_icd = []
        new_hist = []
        strg = ''
        for items in icd:
            for item in items:
                strg = strg + item
            new_icd.append(strg)
            strg = ''
        for items in icdc:
            for item in items:
                strg = strg + item
            new_icd.append(strg)
            strg = ''
        for items in hist:
            for item in items:
                strg = strg + item
            new_hist.append(strg)
            strg = ''

        #Building the form
        self.scrollArea_cd = QtWidgets.QScrollArea(self.tab2_clinical_data)
        self.scrollArea_cd.setGeometry(QtCore.QRect(0, 0, 880, 517))
        self.scrollArea_cd.setWidgetResizable(False)
        self.scrollArea_cd.setObjectName("scrollArea_cd")
        self.scrollArea_cd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_cd.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 770))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        #self.scrollArea_cd.setLayout(self.scrollAreaWidgetContents)
        self.scrollArea_cd.ensureWidgetVisible(self.scrollAreaWidgetContents)
        self.label_LN = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_LN.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label_LN.setObjectName("label_LN")
        self.date_of_birth = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.date_of_birth.setGeometry(QtCore.QRect(140, 50, 171, 31))
        self.date_of_birth.setObjectName("date_of_birth")
        self.Label_age_diagnosis = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_age_diagnosis.setGeometry(QtCore.QRect(340, 100, 141, 17))
        self.Label_age_diagnosis.setObjectName("Label_age_diagnosis")
        self.label_DB = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_DB.setGeometry(QtCore.QRect(10, 55, 101, 21))
        self.label_DB.setObjectName("label_DB")
        self.line_LN = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_LN.setGeometry(QtCore.QRect(140, 10, 171, 25))
        self.line_LN.setObjectName("line_LN")
        self.label_FN = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_FN.setGeometry(QtCore.QRect(340, 10, 81, 21))
        self.label_FN.setObjectName("label_FN")
        self.line_FN = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_FN.setGeometry(QtCore.QRect(470, 10, 171, 25))
        self.line_FN.setObjectName("line_FN")
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(10, 100, 131, 21))
        self.label_8.setObjectName("label_8")
        self.age_diagnosis = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.age_diagnosis.setGeometry(QtCore.QRect(470, 100, 171, 21))
        self.age_diagnosis.setText("")
        self.age_diagnosis.setObjectName("age_diagnosis")
        self.label_BP = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_BP.setGeometry(QtCore.QRect(340, 50, 101, 21))
        self.label_BP.setObjectName("label_BP")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.dateEdit_2.setGeometry(QtCore.QRect(140, 95, 171, 31))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dx_Year = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.dx_Year.setGeometry(QtCore.QRect(780, 100, 171, 21))
        self.dx_Year.setText("")
        self.dx_Year.setObjectName("dx_Year")
        self.line_BP = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_BP.setGeometry(QtCore.QRect(470, 50, 171, 25))
        self.line_BP.setObjectName("line_BP")
        self.gender = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.gender.setGeometry(QtCore.QRect(780, 10, 171, 25))
        self.gender.setObjectName("gender")
        self.gender.addItem("")
        self.gender.addItem("")
        self.gender.addItem("")
        self.gender.addItem("")
        self.Label_dxYear = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_dxYear.setGeometry(QtCore.QRect(690, 100, 91, 20))
        self.Label_dxYear.setObjectName("Label_dxYear")
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_9.setGeometry(QtCore.QRect(690, 10, 81, 21))
        self.label_9.setObjectName("label_9")
        self.line_icd = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_icd.setGeometry(QtCore.QRect(80, 140, 391, 25))
        self.line_icd.setObjectName("line_icd")
        self.M_stage = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.M_stage.setGeometry(QtCore.QRect(570, 190, 81, 25))
        self.M_stage.setObjectName("M_stage")
        self.M_stage.addItem("")
        self.M_stage.addItem("")
        self.M_stage.addItem("")
        self.label_T_stage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_T_stage.setGeometry(QtCore.QRect(10, 190, 81, 21))
        self.label_T_stage.setObjectName("label_T_stage")
        self.Hormone = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Hormone.setGeometry(QtCore.QRect(430, 350, 171, 25))
        self.Hormone.setObjectName("Hormone")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.Hormone.addItem("")
        self.label_Branchy = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Branchy.setGeometry(QtCore.QRect(10, 350, 81, 21))
        self.label_Branchy.setObjectName("label_Branchy")
        self.Overall_Stage = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Overall_Stage.setGeometry(QtCore.QRect(870, 190, 81, 25))
        self.Overall_Stage.setObjectName("Overall_Stage")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Overall_Stage.addItem("")
        self.Surgery = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Surgery.setGeometry(QtCore.QRect(140, 270, 171, 25))
        self.Surgery.setObjectName("Surgery")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.Surgery.addItem("")
        self.label_Immuno = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Immuno.setGeometry(QtCore.QRect(340, 310, 81, 21))
        self.label_Immuno.setObjectName("label_Immuno")
        self.label_Surgery = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Surgery.setGeometry(QtCore.QRect(10, 270, 81, 21))
        self.label_Surgery.setObjectName("label_Surgery")
        self.Branchy = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Branchy.setGeometry(QtCore.QRect(140, 350, 171, 25))
        self.Branchy.setObjectName("Branchy")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.Branchy.addItem("")
        self.label_histology = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_histology.setGeometry(QtCore.QRect(500, 140, 81, 21))
        self.label_histology.setObjectName("label_histology")
        self.label_Overall_Stage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Overall_Stage.setGeometry(QtCore.QRect(760, 190, 101, 21))
        self.label_Overall_Stage.setObjectName("label_Overall_Stage")
        self.label_Hormone = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Hormone.setGeometry(QtCore.QRect(340, 350, 81, 21))
        self.label_Hormone.setObjectName("label_Hormone")
        self.N_stage = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.N_stage.setGeometry(QtCore.QRect(330, 190, 81, 25))
        self.N_stage.setObjectName("N_stage")
        self.N_stage.addItem("")
        self.N_stage.addItem("")
        self.N_stage.addItem("")
        self.N_stage.addItem("")
        self.N_stage.addItem("")
        self.Chemo = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Chemo.setGeometry(QtCore.QRect(140, 310, 171, 25))
        self.Chemo.setObjectName("Chemo")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.Chemo.addItem("")
        self.line_histology = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_histology.setGeometry(QtCore.QRect(580, 140, 371, 25))
        self.line_histology.setObjectName("line_histology")
        self.label_icd = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_icd.setGeometry(QtCore.QRect(10, 140, 81, 21))
        self.label_icd.setObjectName("label_icd")
        self.label_Rad = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Rad.setGeometry(QtCore.QRect(340, 270, 81, 21))
        self.label_Rad.setObjectName("label_Rad")
        self.label_N_Stage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_N_Stage.setGeometry(QtCore.QRect(260, 190, 81, 21))
        self.label_N_Stage.setObjectName("label_N_Stage")
        self.label_Tx_intent = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Tx_intent.setGeometry(QtCore.QRect(10, 230, 81, 21))
        self.label_Tx_intent.setObjectName("label_Tx_intent")
        self.label_Chemo = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Chemo.setGeometry(QtCore.QRect(10, 310, 81, 21))
        self.label_Chemo.setObjectName("label_Chemo")
        self.Immuno = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Immuno.setGeometry(QtCore.QRect(430, 310, 171, 25))
        self.Immuno.setObjectName("Immuno")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.Immuno.addItem("")
        self.label_M_Stage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_M_Stage.setGeometry(QtCore.QRect(500, 190, 81, 21))
        self.label_M_Stage.setObjectName("label_M_Stage")
        self.T_stage = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.T_stage.setGeometry(QtCore.QRect(80, 190, 81, 25))
        self.T_stage.setObjectName("T_stage")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.T_stage.addItem("")
        self.Rad = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Rad.setGeometry(QtCore.QRect(430, 270, 171, 25))
        self.Rad.setObjectName("Rad")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Rad.addItem("")
        self.Tx_intent = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Tx_intent.setGeometry(QtCore.QRect(140, 230, 171, 25))
        self.Tx_intent.setObjectName("Tx_intent")
        self.Tx_intent.addItem("")
        self.Tx_intent.addItem("")
        self.Tx_intent.addItem("")
        self.Tx_intent.addItem("")
        self.Tx_intent.addItem("")
        self.Tx_intent.addItem("")
        self.Cancer_death = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Cancer_death.setGeometry(QtCore.QRect(520, 440, 171, 25))
        self.Cancer_death.setObjectName("Cancer_death")
        self.Cancer_death.addItem("")
        self.Cancer_death.addItem("")
        self.Cancer_death.addItem("")
        self.label_DT_Last_existence = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_DT_Last_existence.setGeometry(QtCore.QRect(10, 395, 171, 21))
        self.label_DT_Last_existence.setObjectName("label_DT_Last_existence")
        self.label_Regional_control = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Regional_control.setGeometry(QtCore.QRect(10, 550, 121, 21))
        self.label_Regional_control.setObjectName("label_Regional_control")
        self.Label_DC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_DC_duration.setGeometry(QtCore.QRect(10, 660, 141, 17))
        self.Label_DC_duration.setObjectName("Label_DC_duration")
        self.Edit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.Edit_button.setGeometry(QtCore.QRect(10, 710, 91, 31))
        self.Edit_button.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
                                       "color: rgb(243, 243, 243);\n"
                                       "background-color: rgb(147, 112, 219);\n"
                                       "")
        self.Edit_button.setObjectName("Edit_button")
        self.scrollArea_cd.ensureWidgetVisible(self.Edit_button)
        self.RC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.RC_duration.setGeometry(QtCore.QRect(140, 590, 171, 21))
        self.RC_duration.setText("")
        self.RC_duration.setObjectName("RC_duration")
        self.label_Distant_Control = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Distant_Control.setGeometry(QtCore.QRect(10, 620, 121, 21))
        self.label_Distant_Control.setObjectName("label_Distant_Control")
        self.label_Cancer_death = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Cancer_death.setGeometry(QtCore.QRect(340, 440, 111, 21))
        self.label_Cancer_death.setObjectName("label_Cancer_death")
        self.label_Dt_Regional_Failure = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Dt_Regional_Failure.setGeometry(QtCore.QRect(340, 555, 171, 21))
        self.label_Dt_Regional_Failure.setObjectName("label_Dt_Regional_Failure")
        self.Distant_Control = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Distant_Control.setGeometry(QtCore.QRect(140, 620, 171, 25))
        self.Distant_Control.setObjectName("Distant_Control")
        self.Distant_Control.addItem("")
        self.Distant_Control.addItem("")
        self.Distant_Control.addItem("")
        self.label_Dt_Distant_Failure = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Dt_Distant_Failure.setGeometry(QtCore.QRect(340, 620, 171, 21))
        self.label_Dt_Distant_Failure.setObjectName("label_Dt_Distant_Failure")
        self.label_Death = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Death.setGeometry(QtCore.QRect(10, 440, 81, 21))
        self.label_Death.setObjectName("label_Death")
        self.label_Local_control = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Local_control.setGeometry(QtCore.QRect(10, 480, 101, 21))
        self.label_Local_control.setObjectName("label_Local_control")
        self.Label_LC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_LC_duration.setGeometry(QtCore.QRect(10, 520, 141, 17))
        self.Label_LC_duration.setObjectName("Label_LC_duration")
        self.label_Dt_Local_failure = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Dt_Local_failure.setGeometry(QtCore.QRect(340, 485, 151, 21))
        self.label_Dt_Local_failure.setObjectName("label_Dt_Local_failure")
        self.Label_survival_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_survival_duration.setGeometry(QtCore.QRect(430, 400, 141, 17))
        self.Label_survival_duration.setObjectName("Label_survival_duration")
        self.DC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.DC_duration.setGeometry(QtCore.QRect(140, 660, 171, 21))
        self.DC_duration.setText("")
        self.DC_duration.setObjectName("DC_duration")
        self.Death = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Death.setGeometry(QtCore.QRect(140, 440, 171, 25))
        self.Death.setObjectName("Death")
        self.Death.addItem("")
        self.Death.addItem("")
        self.Death.addItem("")
        self.Dt_REgional_failure = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.Dt_REgional_failure.setGeometry(QtCore.QRect(520, 550, 171, 31))
        self.Dt_REgional_failure.setObjectName("Dt_REgional_failure")
        self.Regional_Control = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Regional_Control.setGeometry(QtCore.QRect(140, 550, 171, 25))
        self.Regional_Control.setObjectName("Regional_Control")
        self.Regional_Control.addItem("")
        self.Regional_Control.addItem("")
        self.Regional_Control.addItem("")
        self.Dt_Last_Existence = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.Dt_Last_Existence.setGeometry(QtCore.QRect(190, 390, 171, 31))
        self.Dt_Last_Existence.setObjectName("Dt_Last_Existence")
        self.LC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.LC_duration.setGeometry(QtCore.QRect(140, 520, 171, 21))
        self.LC_duration.setText("")
        self.LC_duration.setObjectName("LC_duration")
        self.Label_RC_duration = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Label_RC_duration.setGeometry(QtCore.QRect(10, 590, 141, 17))
        self.Label_RC_duration.setObjectName("Label_RC_duration")
        self.Dt_Distant_Failure = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.Dt_Distant_Failure.setGeometry(QtCore.QRect(520, 615, 171, 31))
        self.Dt_Distant_Failure.setObjectName("Dt_Distant_Failure")
        self.Local_control = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Local_control.setGeometry(QtCore.QRect(140, 480, 171, 25))
        self.Local_control.setObjectName("Local_control")
        self.Local_control.addItem("")
        self.Local_control.addItem("")
        self.Local_control.addItem("")
        self.Dt_local_failure = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.Dt_local_failure.setGeometry(QtCore.QRect(520, 480, 171, 31))
        self.Dt_local_failure.setObjectName("Dt_local_failure")
        self.scrollArea_cd.setWidget(self.scrollAreaWidgetContents)
        self.tab2.addTab(self.tab2_clinical_data, "")

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
        self.gridLayout_struct_info = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_struct_info.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_struct_info.setObjectName("gridLayout_struct_info")

        # Structure Information: Information Icon
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/images/Icon/info.png"))
        self.label_3.setObjectName("label_3")
        self.gridLayout_struct_info.addWidget(self.label_3, 1, 0, 1, 1)

        # Structure Information: Structure Information Label
        self.struct_info_label = QtWidgets.QLabel(self.widget)
        self.struct_info_label.setFont(QtGui.QFont("Laksaman", weight=QtGui.QFont.Bold, pointSize=10))
        self.struct_info_label.setObjectName("struct_info_label")
        self.gridLayout_struct_info.addWidget(self.struct_info_label, 1, 1, 1, 1)

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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Icon/open_patient.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionOpen.setIcon(icon)
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
        self.actionWindowingNormal = QtWidgets.QAction(MainWindow)
        self.actionWindowingNormal.setObjectName("actionWindowingNormal")
        self.actionWindowingLung = QtWidgets.QAction(MainWindow)
        self.actionWindowingLung.setObjectName("actionWindowingLung")
        self.actionWindowingBone = QtWidgets.QAction(MainWindow)
        self.actionWindowingBone.setObjectName("actionWindowingBone")
        self.actionWindowingSoftTissue = QtWidgets.QAction(MainWindow)
        self.actionWindowingSoftTissue.setObjectName("actionWindowingSoftTissue")
        self.actionWindowingBrain = QtWidgets.QAction(MainWindow)
        self.actionWindowingBrain.setObjectName("actionWindowingBrain")

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
        # self.actionAnonymize_and_Save.triggered.connect(self.pluginMenu)


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
        self.menuWindowing.addAction(self.actionWindowingNormal)
        self.menuWindowing.addAction(self.actionWindowingBone)
        self.menuWindowing.addAction(self.actionWindowingBrain)
        self.menuWindowing.addAction(self.actionWindowingLung)
        self.menuWindowing.addAction(self.actionWindowingSoftTissue)
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
        self.label_LN.setText(_translate("MainWindow", "Last Name:"))
        self.Label_age_diagnosis.setText(_translate("MainWindow", "Age at Diagnosis:"))
        self.label_DB.setText(_translate("MainWindow", "Date of Birth:"))
        self.label_FN.setText(_translate("MainWindow", "First Name:"))
        self.label_8.setText(_translate("MainWindow", "Date of Diagnosis:"))
        self.label_BP.setText(_translate("MainWindow", "Birth Country:"))
        self.gender.setItemText(0, _translate("MainWindow", "Select..."))
        self.gender.setItemText(1, _translate("MainWindow", "F"))
        self.gender.setItemText(2, _translate("MainWindow", "M"))
        self.gender.setItemText(3, _translate("MainWindow", "O"))
        self.Label_dxYear.setText(_translate("MainWindow", "DxYear:"))
        self.label_9.setText(_translate("MainWindow", "Gender:"))
        self.M_stage.setItemText(0, _translate("MainWindow", "Select..."))
        self.M_stage.setItemText(1, _translate("MainWindow", "M0"))
        self.M_stage.setItemText(2, _translate("MainWindow", "M1"))
        self.label_T_stage.setText(_translate("MainWindow", "T Stage:"))
        self.Hormone.setItemText(0, _translate("MainWindow", "Select..."))
        self.Hormone.setItemText(1, _translate("MainWindow", "No"))
        self.Hormone.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Hormone.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Hormone.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Hormone.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Hormone.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Hormone.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Hormone.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Hormone.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Hormone.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Hormone.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Hormone.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.label_Branchy.setText(_translate("MainWindow", "Brachy:"))
        self.Overall_Stage.setItemText(0, _translate("MainWindow", "Select..."))
        self.Overall_Stage.setItemText(1, _translate("MainWindow", "O"))
        self.Overall_Stage.setItemText(2, _translate("MainWindow", "I"))
        self.Overall_Stage.setItemText(3, _translate("MainWindow", "IA"))
        self.Overall_Stage.setItemText(4, _translate("MainWindow", "IB"))
        self.Overall_Stage.setItemText(5, _translate("MainWindow", "II"))
        self.Overall_Stage.setItemText(6, _translate("MainWindow", "IIA"))
        self.Overall_Stage.setItemText(7, _translate("MainWindow", "IIB"))
        self.Overall_Stage.setItemText(8, _translate("MainWindow", "III"))
        self.Overall_Stage.setItemText(9, _translate("MainWindow", "IIIA"))
        self.Overall_Stage.setItemText(10, _translate("MainWindow", "IIIB"))
        self.Overall_Stage.setItemText(11, _translate("MainWindow", "IIIC"))
        self.Overall_Stage.setItemText(12, _translate("MainWindow", "IV"))
        self.Overall_Stage.setItemText(13, _translate("MainWindow", "IVA"))
        self.Overall_Stage.setItemText(14, _translate("MainWindow", "IVB"))
        self.Overall_Stage.setItemText(15, _translate("MainWindow", "IVC"))
        self.Surgery.setItemText(0, _translate("MainWindow", "Select..."))
        self.Surgery.setItemText(1, _translate("MainWindow", "No"))
        self.Surgery.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Surgery.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Surgery.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Surgery.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Surgery.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Surgery.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Surgery.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Surgery.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Surgery.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Surgery.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Surgery.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.label_Immuno.setText(_translate("MainWindow", "Immuno:"))
        self.label_Surgery.setText(_translate("MainWindow", "Surgery:"))
        self.Branchy.setItemText(0, _translate("MainWindow", "Select..."))
        self.Branchy.setItemText(1, _translate("MainWindow", "No"))
        self.Branchy.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Branchy.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Branchy.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Branchy.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Branchy.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Branchy.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Branchy.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Branchy.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Branchy.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Branchy.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Branchy.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.label_histology.setText(_translate("MainWindow", "Histology:"))
        self.label_Overall_Stage.setText(_translate("MainWindow", "Overall Stage:"))
        self.label_Hormone.setText(_translate("MainWindow", "Hormone:"))
        self.N_stage.setItemText(0, _translate("MainWindow", "Select..."))
        self.N_stage.setItemText(1, _translate("MainWindow", "N0"))
        self.N_stage.setItemText(2, _translate("MainWindow", "N1"))
        self.N_stage.setItemText(3, _translate("MainWindow", "N2"))
        self.N_stage.setItemText(4, _translate("MainWindow", "N3"))
        self.Chemo.setItemText(0, _translate("MainWindow", "Select..."))
        self.Chemo.setItemText(1, _translate("MainWindow", "No"))
        self.Chemo.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Chemo.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Chemo.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Chemo.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Chemo.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Chemo.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Chemo.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Chemo.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Chemo.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Chemo.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Chemo.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.label_icd.setText(_translate("MainWindow", "ICD10:"))
        self.label_Rad.setText(_translate("MainWindow", "Rad:"))
        self.label_N_Stage.setText(_translate("MainWindow", "N Stage:"))
        self.label_Tx_intent.setText(_translate("MainWindow", "Tx_Intent:"))
        self.label_Chemo.setText(_translate("MainWindow", "Chemo:"))
        self.Immuno.setItemText(0, _translate("MainWindow", "Select..."))
        self.Immuno.setItemText(1, _translate("MainWindow", "No"))
        self.Immuno.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Immuno.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Immuno.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Immuno.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Immuno.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Immuno.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Immuno.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Immuno.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Immuno.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Immuno.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Immuno.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.label_M_Stage.setText(_translate("MainWindow", "M Stage:"))
        self.T_stage.setItemText(0, _translate("MainWindow", "Select..."))
        self.T_stage.setItemText(1, _translate("MainWindow", "T0"))
        self.T_stage.setItemText(2, _translate("MainWindow", "Tis"))
        self.T_stage.setItemText(3, _translate("MainWindow", "T1"))
        self.T_stage.setItemText(4, _translate("MainWindow", "T2"))
        self.T_stage.setItemText(5, _translate("MainWindow", "T3"))
        self.T_stage.setItemText(6, _translate("MainWindow", "T4"))
        self.Rad.setItemText(0, _translate("MainWindow", "Select..."))
        self.Rad.setItemText(1, _translate("MainWindow", "No"))
        self.Rad.setItemText(2, _translate("MainWindow", "Primary (Pri)"))
        self.Rad.setItemText(3, _translate("MainWindow", "Refused (Ref)"))
        self.Rad.setItemText(4, _translate("MainWindow", "Denied (Den)"))
        self.Rad.setItemText(5, _translate("MainWindow", "DiedB4 (Die)"))
        self.Rad.setItemText(6, _translate("MainWindow", "Neoadjuvant (Neo)"))
        self.Rad.setItemText(7, _translate("MainWindow", "Concurrent (Con)"))
        self.Rad.setItemText(8, _translate("MainWindow", "Adjuvant (Adj)"))
        self.Rad.setItemText(9, _translate("MainWindow", "Neo&Con"))
        self.Rad.setItemText(10, _translate("MainWindow", "Neo&Adj"))
        self.Rad.setItemText(11, _translate("MainWindow", "Con&Adj"))
        self.Rad.setItemText(12, _translate("MainWindow", "Neo&Con&Adj"))
        self.Tx_intent.setItemText(0, _translate("MainWindow", "Select..."))
        self.Tx_intent.setItemText(1, _translate("MainWindow", "Cure"))
        self.Tx_intent.setItemText(2, _translate("MainWindow", "Palliation"))
        self.Tx_intent.setItemText(3, _translate("MainWindow", "Surveillance"))
        self.Tx_intent.setItemText(4, _translate("MainWindow", "Refused"))
        self.Tx_intent.setItemText(5, _translate("MainWindow", "DiedB4"))
        self.Cancer_death.setItemText(0, _translate("MainWindow", "Select..."))
        self.Cancer_death.setItemText(1, _translate("MainWindow", "0"))
        self.Cancer_death.setItemText(2, _translate("MainWindow", "1"))
        self.label_DT_Last_existence.setText(_translate("MainWindow", "Date of Last Existence:"))
        self.label_Regional_control.setText(_translate("MainWindow", "Regional Control:"))
        self.Label_DC_duration.setText(_translate("MainWindow", "DC Duration:"))
        self.Edit_button.setText(_translate("MainWindow", "Edit"))
        self.label_Distant_Control.setText(_translate("MainWindow", "Distant Control:"))
        self.label_Cancer_death.setText(_translate("MainWindow", "Cancer Death:"))
        self.label_Dt_Regional_Failure.setText(_translate("MainWindow", "Date of Regional Failure:"))
        self.Distant_Control.setItemText(0, _translate("MainWindow", "Select..."))
        self.Distant_Control.setItemText(1, _translate("MainWindow", "0"))
        self.Distant_Control.setItemText(2, _translate("MainWindow", "1"))
        self.label_Dt_Distant_Failure.setText(_translate("MainWindow", "Date of Distant Failure:"))
        self.label_Death.setText(_translate("MainWindow", "Death:"))
        self.label_Local_control.setText(_translate("MainWindow", "Local Control:"))
        self.Label_LC_duration.setText(_translate("MainWindow", "LC Duration:"))
        self.label_Dt_Local_failure.setText(_translate("MainWindow", "Date of Local Failure:"))
        self.Label_survival_duration.setText(_translate("MainWindow", "Survival Duration:"))
        self.Death.setItemText(0, _translate("MainWindow", "Select..."))
        self.Death.setItemText(1, _translate("MainWindow", "0"))
        self.Death.setItemText(2, _translate("MainWindow", "1"))
        self.Regional_Control.setItemText(0, _translate("MainWindow", "Select..."))
        self.Regional_Control.setItemText(1, _translate("MainWindow", "0"))
        self.Regional_Control.setItemText(2, _translate("MainWindow", "1"))
        self.Label_RC_duration.setText(_translate("MainWindow", "RC Duration:"))
        self.Local_control.setItemText(0, _translate("MainWindow", "Select..."))
        self.Local_control.setItemText(1, _translate("MainWindow", "0"))
        self.Local_control.setItemText(2, _translate("MainWindow", "1"))
        self.tab2.setTabText(self.tab2.indexOf(self.tab2_clinical_data), _translate("MainWindow", "Clinical Data"))

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
        self.actionWindowingNormal.setText(_translate("MainWindow", "Normal"))
        self.actionWindowingLung.setText(_translate("MainWindow", "Lung"))
        self.actionWindowingBone.setText(_translate("MainWindow", "Bone"))
        self.actionWindowingSoftTissue.setText(_translate("MainWindow", "Soft Tissue"))
        self.actionWindowingBrain.setText(_translate("MainWindow", "Brain"))
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

        self.frame_structures = QtWidgets.QFrame(self.scrollAreaStruct)
        self.frame_structures.setLayout(QtWidgets.QVBoxLayout())
        self.scrollAreaStruct.setWidget(self.frame_structures)
        self.frame_structures.layout().setContentsMargins(0, 0, 0, 0)

        # self.scrollAreaStruct = QtWidgets.QScrollArea(self.tab1_structures)
        # self.scrollAreaStruct.setWidgetResizable(False)
        # self.scrollAreaStruct.setGeometry(QtCore.QRect(0, 0, 200, 333))
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

        self.dictCheckBoxStruct = dict()
        index = 0

        for key, value in self.rois.items():
            # checkBoxStruct = QtWidgets.QCheckBox(self.scrollContentsStruct)
            checkBoxStruct = QtWidgets.QCheckBox(value['name'])
            checkBoxStruct.clicked.connect(
                lambda: print(value['name']) if checkBoxStruct.isChecked() == True
                        else print(value['name']))
            checkBoxStruct.setStyleSheet("font: 10pt \"Laksaman\";")
            self.frame_structures.layout().addWidget(checkBoxStruct)
            self.dictCheckBoxStruct[value['name']] = checkBoxStruct



    def checkBoxState(self):
        print(self.dictCheckBoxStruct)
        print(self.sender().text())
        text = self.sender().text()
        pressedCheckBox = self.dictCheckBoxStruct[text]
        if pressedCheckBox.isChecked() == True:
            self.selected_rois.append(text)
            print(self.selected_rois)

        else:
            self.selected_rois.remove(text)
            print(self.selected_rois)



    # In the Model directory
    def getDVH(self):
        res = calc_dvhs(self.dataset_rtss, self.dataset_rtdose, self.rois)
        return res


    # In the View directory
    def DVH_view(self, dvh_file):
        fig, ax = plt.subplots()
        fig.subplots_adjust(0.1, 0.15, 1, 1)
        max_xlim = 0
        for roi, dvh in dvh_file.items():
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


    # When the value of the slider in the DICOM View changes
    def valueChangeSlider(self):
        id = self.slider.value()
        # Update DICOM View
        pixmap = self.pixmaps[id]
        pixmap = pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio)
        DICOM_image_label = QtWidgets.QLabel()
        DICOM_image_label.setPixmap(pixmap)
        DICOM_image_scene = QtWidgets.QGraphicsScene()
        DICOM_image_scene.addWidget(DICOM_image_label)
        self.DICOM_view.setScene(DICOM_image_scene)
        # # Update DICOM Tree
        # self.modelTree.endResetModel()
        # self.updateTreeModel(id)
        pass


    def createTreeModel(self):
        self.NAME, self.VALUE, self.TAG, self.VM, self.VR = range(5)
        self.modelTree = QtGui.QStandardItemModel(0, 5)
        self.modelTree.setHeaderData(self.NAME, QtCore.Qt.Horizontal, "Name")
        self.modelTree.setHeaderData(self.VALUE, QtCore.Qt.Horizontal, "Value")
        self.modelTree.setHeaderData(self.TAG, QtCore.Qt.Horizontal, "Tag")
        self.modelTree.setHeaderData(self.VM, QtCore.Qt.Horizontal, "VM")
        self.modelTree.setHeaderData(self.VR, QtCore.Qt.Horizontal, "VR")

    def updateTreeModel(self, id):
        filename = self.path + '/ct.' + str(id) + '.dcm'
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

    def pyradiomicsHandler(self):
        self.callClass.runPyradiomics()


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