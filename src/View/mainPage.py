import matplotlib.pylab as plt
from copy import deepcopy
from PyQt5.QtGui import QTransform
from src.Controller.pluginMController import PManager
from src.Model.CalculateDVHs import calc_dvhs
from src.Model.CalculateImages import *
from src.Model.GetPatientInfo import *
from src.Controller.mainPageController import MainPage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Ui_MainWindow(object):

    def setupUi(self, MainWindow, path):

        ##############################
        #  LOAD PATIENT INFORMATION  #
        ##############################

        self.path = path
        self.dataset, self.filepaths = get_datasets(path)

        self.window = self.dataset[0].WindowWidth[1]
        self.level = self.dataset[0].WindowCenter[1]
        self.x1, self.y1 = 256, 256
        self.dict_windowing = {"normal": [self.window, self.level], "lung": [1600, -300], "bone": [1400, 700],
                               "brain": [180, 950],
                               "soft tissue": [400, 800], "head and neck": [275, 900]}

        self.pixel_values = convert_raw_data(self.dataset)
        self.pixmaps = get_pixmaps(self.pixel_values, self.window, self.level)

        self.file_rtss = self.filepaths['rtss']
        self.file_rtdose = self.filepaths['rtdose']
        self.dataset_rtss = pydicom.dcmread(self.file_rtss)
        self.dataset_rtdose = pydicom.dcmread(self.file_rtdose)
        self.rois = get_roi_info(self.dataset_rtss)
        self.listRoisID = self.orderedListRoiID()
        self.selected_rois = []
        self.dvh = calc_dvhs(self.dataset_rtss, self.dataset_rtdose, self.rois)
        self.roi_info = StructureInformation(self)
        self.basicInfo = get_basic_info(self.dataset[0])

        self.zoom = 1

        # DICOM Tree for RTSS file
        self.dicomTree_rtss = DicomTree(self.file_rtss)
        self.dictDicomTree_rtss = self.dicomTree_rtss.dict

        # DICOM Tree for RT Dose file
        self.dicomTree_rtdose = DicomTree(self.file_rtdose)
        self.dictDicomTree_rtdose = self.dicomTree_rtdose.dict

        self.callClass = MainPage(self.path, self.dataset, self.filepaths)
        self.callManager = PManager()


        ##########################################
        #  IMPLEMENTATION OF THE MAIN PAGE VIEW  #
        ##########################################

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
        self.initStructCol()
        self.updateStructCol()
        self.tab1.addTab(self.tab1_structures, "")

        # Left Column: Isodoses tab
        self.initIsodColumn()
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
        self.initSlider()
        self.gridLayout_view.addWidget(self.slider, 0, 1, 1, 1)
        # DICOM image processing
        self.initDICOM_view()
        self.DICOM_image_display()
        self.textOnDICOM_View()
        self.DICOM_view.setScene(self.DICOM_image_scene)
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
        self.initExportDVH()

        self.tab2.addTab(self.tab2_DVH, "")

        # Main view: DICOM Tree
        self.tab2_DICOM_tree = QtWidgets.QWidget()
        self.tab2_DICOM_tree.setObjectName("tab2_DICOM_tree")
        # Tree View tab grid layout
        self.vboxL_Tree = QtWidgets.QVBoxLayout(self.tab2_DICOM_tree)
        self.vboxL_Tree.setObjectName("vboxL_Tree")
        self.vboxL_Tree.setContentsMargins(0, 0, 0, 0)

        # Tree view selector
        self.initTreeViewSelector()
        # Creation of the Tree View
        self.treeView = QtWidgets.QTreeView(self.tab2_DICOM_tree)
        self.initTree()
        self.initTreeParameters()
        self.tab2.addTab(self.tab2_DICOM_tree, "")

        # Main view: Clinical Data
        self.tab2_clinical_data = QtWidgets.QWidget()
        # check for csv data
        reg = '/[clinicaldata]*[.csv]'
        if not glob.glob(self.path + reg):
            self.callClass.display_cd_form(self.tab2, self.path)
        else:
            self.callClass.display_cd_dat(self.tab2, self.path)

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
        self.initStructInfoSelector()

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
        self.struct_volume_box.setGeometry(QtCore.QRect(95, 70, 81, 31))
        self.struct_volume_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_volume_box.setObjectName("struct_volume_box")

        # Structure Information: "Min Dose" box
        self.struct_minDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_minDose_box.setGeometry(QtCore.QRect(95, 100, 81, 31))
        self.struct_minDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_minDose_box.setObjectName("struct_minDose_box")

        # Structure Information: "Max Dose" box
        self.struct_maxDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_maxDose_box.setGeometry(QtCore.QRect(95, 130, 81, 31))
        self.struct_maxDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_maxDose_box.setObjectName("struct_maxDose_box")

        # Structure Information: "Mean Dose" box
        self.struct_meanDose_box = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_meanDose_box.setGeometry(QtCore.QRect(95, 160, 81, 31))
        self.struct_meanDose_box.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_meanDose_box.setObjectName("struct_meanDose_box")

        # Structure Information: "Volume" unit
        self.struct_volume_unit = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_volume_unit.setGeometry(QtCore.QRect(160, 70, 81, 31))
        self.struct_volume_unit.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_volume_unit.setObjectName("struct_volume_unit")

        # Structure Information: "Min Dose" unit
        self.struct_minDose_unit = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_minDose_unit.setGeometry(QtCore.QRect(160, 100, 81, 31))
        self.struct_minDose_unit.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_minDose_unit.setObjectName("struct_minDose_unit")

        # Structure Information: "Max Dose" unit
        self.struct_maxDose_unit = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_maxDose_unit.setGeometry(QtCore.QRect(160, 130, 81, 31))
        self.struct_maxDose_unit.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_maxDose_unit.setObjectName("struct_maxDose_unit")

        # Structure Information: "Mean Dose" unit
        self.struct_meanDose_unit = QtWidgets.QLabel(self.frame_struct_info)
        self.struct_meanDose_unit.setGeometry(QtCore.QRect(160, 160, 81, 31))
        self.struct_meanDose_unit.setStyleSheet("font: 10pt \"Laksaman\";")
        self.struct_meanDose_unit.setObjectName("struct_meanDose_unit")

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
        self.struct_volume_unit.raise_()
        self.struct_minDose_unit.raise_()
        self.struct_maxDose_unit.raise_()
        self.struct_meanDose_unit.raise_()

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
        self.actionZoom_In.triggered.connect(self.zoomIn)

        # Zoom Out Action
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)

        self.actionZoom_Out.setIcon(iconZoom_Out)
        self.actionZoom_Out.setIconVisibleInMenu(True)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        self.actionZoom_Out.triggered.connect(self.zoomOut)

        # Windowing Action
        self.actionWindowing = QtWidgets.QAction(MainWindow)
        self.actionWindowing.setIcon(iconWindowing)
        self.actionWindowing.setIconVisibleInMenu(True)
        self.actionWindowing.setObjectName("actionWindowing")
        self.initWindowingMenu(MainWindow)

        # Transect Action
        self.actionTransect = QtWidgets.QAction(MainWindow)
        self.actionTransect.setIcon(iconTransect)
        self.actionTransect.setIconVisibleInMenu(True)
        self.actionTransect.setObjectName("actionTransect")
        self.actionTransect.triggered.connect(self.transectHandler)

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
        self.actionPlugin_Manager.triggered.connect(self.pluginManagerHandler)

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
        self.struct_volume_label.setText(_translate("MainWindow", "Volume:"))
        self.struct_minDose_label.setText(_translate("MainWindow", "Min Dose:"))
        self.struct_maxDose_label.setText(_translate("MainWindow", "Max Dose:"))
        self.struct_meanDose_label.setText(_translate("MainWindow", "Mean Dose:"))
        self.struct_info_label.setText(_translate("MainWindow", "Structure Information"))

        # # Set structure information units
        self.struct_volume_unit.setText(_translate("MainWindow", "cm³"))
        self.struct_minDose_unit.setText(_translate("MainWindow", "cGy"))
        self.struct_maxDose_unit.setText(_translate("MainWindow", "cGy"))
        self.struct_meanDose_unit.setText(_translate("MainWindow", "cGy"))

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
        self.actionTransect.setText(_translate("MainWindow", "Transect"))
        self.actionBrush.setText(_translate("MainWindow", "ROI by Brush"))
        self.actionIsodose.setText(_translate("MainWindow", "ROI by Isodose"))
        self.actionPlugin_Manager.setText(_translate("MainWindow", "Plugin Manager..."))
        self.actionAnonymize_and_Save.setText(_translate("MainWindow", "Anonymize and Save"))
        self.actionDVH_Spreadsheet.setText(_translate("MainWindow", "DVH"))
        self.actionClinical_Data.setText(_translate("MainWindow", "Clinical Data"))
        self.actionPyradiomics.setText(_translate("MainWindow", "Pyradiomics"))

        MainWindow.update()


    def orderedListRoiID(self):
        res = []
        for id, value in self.rois.items():
            res.append(id)
        return sorted(res)

    ########################
    #  ZOOM FUNCTIONALITY  #
    ########################

    def zoomIn(self):

        self.zoom *= 1.05
        self.updateView()

    def zoomOut(self):

        self.zoom /= 1.05
        self.updateView()

    def updateView(self):
        self.DICOM_image_display()
        self.textOnDICOM_View()
        self.DICOM_view.setTransform(QTransform().scale(self.zoom, self.zoom))
        self.DICOM_view.setScene(self.DICOM_image_scene)


    #################################
    #  STRUCTURES AND ISODOSES TAB  #
    #################################

    # Initialization of colors for ROIs
    def initRoiColor(self):
        self.allColor = HexaColor()
        self.roiColor = dict()
        index = 0
        for key, val in self.rois.items():
            value = dict()
            value['R'], value['G'], value['B'] = self.allColor.getHexaColor(index)
            value['QColor'] = QtGui.QColor(value['R'], value['G'], value['B'])
            self.roiColor[key] = value
            index += 1

    # Initialization of the list of structures (left column of the main page)
    def initStructCol(self):
        # Color squares initialization for each ROI
        self.initRoiColor()
        # Scroll Area
        self.tab1_structures = QtWidgets.QWidget()
        self.tab1_structures.setObjectName("tab1_structures")
        self.structColumnWidget = QtWidgets.QWidget(self.tab1_structures)
        self.scrollAreaStruct = QtWidgets.QScrollArea(self.structColumnWidget)
        self.scrollAreaStruct.setGeometry(QtCore.QRect(0, 0, 198, 320))
        self.scrollAreaStruct.setWidgetResizable(True)
        # Scroll Area Content
        self.scrollAreaStructContents = QtWidgets.QWidget(self.scrollAreaStruct)
        self.scrollAreaStructContents.setGeometry(QtCore.QRect(0, 0, 198, 550))
        self.scrollAreaStruct.ensureWidgetVisible(self.scrollAreaStructContents)
        # Grid Layout containing the color squares and the checkboxes
        self.gridL_StructColumn = QtWidgets.QGridLayout(self.scrollAreaStructContents)
        self.gridL_StructColumn.setContentsMargins(5, 5, 5, 5)
        self.gridL_StructColumn.setVerticalSpacing(0)
        self.gridL_StructColumn.setHorizontalSpacing(10)
        self.gridL_StructColumn.setObjectName("gridL_StructColumn")

    # Add the contents in the list of structures (left column of the main page)
    def updateStructCol(self):
        index = 0
        for key, value in self.rois.items():
            # Color Square
            colorSquareLabel = QtWidgets.QLabel()
            colorSquarePix = QtGui.QPixmap(15, 15)
            colorSquarePix.fill(self.roiColor[key]['QColor'])
            colorSquareLabel.setPixmap(colorSquarePix)
            self.gridL_StructColumn.addWidget(colorSquareLabel, index, 0, 1, 1)
            # QCheckbox
            text = value['name']
            checkBoxStruct = QtWidgets.QCheckBox()
            checkBoxStruct.clicked.connect(
                lambda state, text=key: self.checkedStruct(state, text))
            checkBoxStruct.setStyleSheet("font: 10pt \"Laksaman\";")
            checkBoxStruct.setText(text)
            checkBoxStruct.setObjectName(text)
            self.gridL_StructColumn.addWidget(checkBoxStruct, index, 1, 1, 1)
            index += 1
        self.scrollAreaStruct.setStyleSheet("QScrollArea {background-color: #ffffff; border-style: none;}")
        self.scrollAreaStructContents.setStyleSheet("QWidget {background-color: #ffffff; border-style: none;}")

        vspacer = QtWidgets.QSpacerItem(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridL_StructColumn.addItem(vspacer, index + 1, 0, 1, -1)

        hspacer = QtWidgets.QSpacerItem(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridL_StructColumn.addItem(hspacer, 0, 2, -1, 1)

        self.scrollAreaStruct.setWidget(self.scrollAreaStructContents)

    # Update the list of selected structures and DVH view
    def checkedStruct(self, state, text):
        if state:
            self.selected_rois.append(text)
        else:
            self.selected_rois.remove(text)
        self.updateDVH_view()

    # Initialize the list of isodoses (left column of the main page)
    def initIsodColumn(self):
        self.tab1_isodoses = QtWidgets.QWidget()
        self.tab1_isodoses.setGeometry(QtCore.QRect(0, 0, 198, 320))
        self.gridL_IsodCol = QtWidgets.QGridLayout(self.tab1_isodoses)
        self.gridL_IsodCol.setContentsMargins(5, 1, 0, 0)
        self.gridL_IsodCol.setVerticalSpacing(1)
        self.gridL_IsodCol.setHorizontalSpacing(10)
        self.gridL_IsodCol.setObjectName("gridL_IsodCol")
        # Color squares
        self.color1_isod = self.colorSquareDraw(131, 0, 0)
        self.color2_isod = self.colorSquareDraw(185, 0, 0)
        self.color3_isod = self.colorSquareDraw(255, 46, 0)
        self.color4_isod = self.colorSquareDraw(255, 161, 0)
        self.color5_isod = self.colorSquareDraw(253, 255, 0)
        self.color6_isod = self.colorSquareDraw(0, 255, 0)
        self.color7_isod = self.colorSquareDraw(0, 143, 0)
        self.color8_isod = self.colorSquareDraw(0, 255, 255)
        self.color9_isod = self.colorSquareDraw(33, 0, 255)
        self.color10_isod = self.colorSquareDraw(11, 0, 134)
        self.gridL_IsodCol.addWidget(self.color1_isod, 0, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color2_isod, 1, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color3_isod, 2, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color4_isod, 3, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color5_isod, 4, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color6_isod, 5, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color7_isod, 6, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color8_isod, 7, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color9_isod, 8, 0, 1, 1)
        self.gridL_IsodCol.addWidget(self.color10_isod, 9, 0, 1, 1)
        # Checkboxes
        self.isodose_patient = 7000
        val_isod1 = int(1.07 * self.isodose_patient)
        val_isod2 = int(1.05 * self.isodose_patient)
        val_isod3 = int(1.00 * self.isodose_patient)
        val_isod4 = int(0.95 * self.isodose_patient)
        val_isod5 = int(0.90 * self.isodose_patient)
        val_isod6 = int(0.80 * self.isodose_patient)
        val_isod7 = int(0.70 * self.isodose_patient)
        val_isod8 = int(0.60 * self.isodose_patient)
        val_isod9 = int(0.30 * self.isodose_patient)
        val_isod10 = int(0.10 * self.isodose_patient)
        self.box1_isod = QtWidgets.QCheckBox("107 % / " + str(val_isod1) + " cGy [Max]")
        self.box2_isod = QtWidgets.QCheckBox("105 % / " + str(val_isod2) + " cGy")
        self.box3_isod = QtWidgets.QCheckBox("100 % / " + str(val_isod3) + " cGy")
        self.box4_isod = QtWidgets.QCheckBox("95 % / " + str(val_isod4) + " cGy")
        self.box5_isod = QtWidgets.QCheckBox("90 % / " + str(val_isod5) + " cGy")
        self.box6_isod = QtWidgets.QCheckBox("80 % / " + str(val_isod6) + " cGy")
        self.box7_isod = QtWidgets.QCheckBox("70 % / " + str(val_isod7) + " cGy")
        self.box8_isod = QtWidgets.QCheckBox("60 % / " + str(val_isod8) + " cGy")
        self.box9_isod = QtWidgets.QCheckBox("30 % / " + str(val_isod9) + " cGy")
        self.box10_isod = QtWidgets.QCheckBox("10 % / " + str(val_isod10) + " cGy")
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
        self.gridL_IsodCol.addWidget(self.box1_isod, 0, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box2_isod, 1, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box3_isod, 2, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box4_isod, 3, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box5_isod, 4, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box6_isod, 5, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box7_isod, 6, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box8_isod, 7, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box9_isod, 8, 1, 1, 1)
        self.gridL_IsodCol.addWidget(self.box10_isod, 9, 1, 1, 1)

        vspacer = QtWidgets.QSpacerItem(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gridL_IsodCol.addItem(vspacer, 10, 0, 2, -1)

    # Draw color squares
    def colorSquareDraw(self, a, b, c):
        colorSquareLabel = QtWidgets.QLabel()
        colorSquarePix = QtGui.QPixmap(15, 15)
        colorSquarePix.fill(QtGui.QColor(a, b, c))
        colorSquareLabel.setPixmap(colorSquarePix)
        return colorSquareLabel


    ###########################
    #  STRUCTURE INFORMATION  #
    ###########################

    # Initialize the selector for structure information
    def initStructInfoSelector(self):
        self.comboBox = QtWidgets.QComboBox(self.frame_struct_info)
        self.comboBox.setStyleSheet("QComboBox {font: 75 10pt \"Laksaman\";"
                                                 "combobox-popup: 0;"
                                                 "background-color: #efefef; }")
        self.comboBox.addItem("Select...")
        for key, value in self.rois.items():
            self.comboBox.addItem(value['name'])
        self.comboBox.activated.connect(self.comboStructInfo)
        self.comboBox.setGeometry(QtCore.QRect(5, 35, 188, 31))
        self.comboBox.setObjectName("comboBox")

    # Function triggered when an item is selected
    def comboStructInfo(self, index):
        _translate = QtCore.QCoreApplication.translate

        if index == 0:
            self.struct_volume_box.setText(_translate("MainWindow", "-"))
            self.struct_minDose_box.setText(_translate("MainWindow", "-"))
            self.struct_maxDose_box.setText(_translate("MainWindow", "-"))
            self.struct_meanDose_box.setText(_translate("MainWindow", "-"))

        else:
            structID = self.listRoisID[index-1]

            # Set structure information boxes
            self.struct_volume_box.setText(_translate("MainWindow", str(self.roi_info.getVolume(structID))))
            self.struct_minDose_box.setText(_translate("MainWindow", str(self.roi_info.getMin(structID))))
            self.struct_maxDose_box.setText(_translate("MainWindow", str(self.roi_info.getMax(structID))))
            self.struct_meanDose_box.setText(_translate("MainWindow", str(self.roi_info.getMean(structID))))


    #######################
    #  DVH FUNCTIONALITY  #
    #######################

    def DVH_view(self):
        fig, ax = plt.subplots()
        fig.subplots_adjust(0.1, 0.15, 1, 1)
        max_xlim = 0
        for roi in self.selected_rois:
            dvh = self.dvh[int(roi)]
            if dvh.volume != 0:
                colorRoi = self.roiColor[roi]
                color_R = colorRoi['R'] / 255
                color_G = colorRoi['G'] / 255
                color_B = colorRoi['B'] / 255
                plt.plot(100 * dvh.bincenters, 100 * dvh.counts / dvh.volume, label=dvh.name,
                         color=[color_R, color_G, color_B])
                if (100 * dvh.bincenters[-1]) > max_xlim:
                    max_xlim = 100 * dvh.bincenters[-1]
                plt.xlabel('Dose [%s]' % 'cGy')
                plt.ylabel('Volume [%s]' % '%')
                if dvh.name:
                    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        ax.set_ylim([0, 105])
        ax.set_xlim([0, max_xlim + 3])

        major_ticks_y = np.arange(0, 105, 20)
        minor_ticks_y = np.arange(0, 105, 5)
        major_ticks_x = np.arange(0, max_xlim + 250, 1000)
        minor_ticks_x = np.arange(0, max_xlim + 250, 250)

        ax.set_xticks(major_ticks_x)
        ax.set_xticks(minor_ticks_x, minor=True)
        ax.set_yticks(major_ticks_y)
        ax.set_yticks(minor_ticks_y, minor=True)

        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        # self.export_legend(legend)

        return fig

    # def export_legend(self, legend, filename="legend.png", expand=[-5, -5, 5, 5]):
    #     fig = legend.figure
    #     fig.canvas.draw()
    #     bbox = legend.get_window_extent()
    #     bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    #     bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    #     fig.savefig(filename, dpi="figure", bbox_inches=bbox)

    def initDVH_view(self):
        fig = self.DVH_view()
        self.plotWidget = FigureCanvas(fig)
        self.gridL_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)


    def updateDVH_view(self):
        self.gridL_DVH.removeWidget(self.plotWidget)
        fig = self.DVH_view()
        self.plotWidget = FigureCanvas(fig)
        self.gridL_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)


    def initExportDVH(self):
        self.button_exportDVH = QtWidgets.QPushButton()
        self.button_exportDVH.setFixedSize(QtCore.QSize(100, 39))
        self.button_exportDVH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportDVH.setStyleSheet("background-color: rgb(238, 238, 236);\n"
                                            "font: 57 11pt \"Ubuntu\";\n"
                                            "color:rgb(75,0,130);\n"
                                            "font-weight: bold;\n")
        self.button_exportDVH.setObjectName("button_exportDVH")
        self.gridL_DVH.addWidget(self.button_exportDVH, 1, 1, 1, 1, QtCore.Qt.AlignBottom)


    ####################################
    #  DICOM IMAGE VIEW FUNCTIONALITY  #
    ####################################

    def initSlider(self):
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


    def initDICOM_view(self):
        self.DICOM_view = QtWidgets.QGraphicsView(self.tab2_view)
        background_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0), QtCore.Qt.SolidPattern)
        self.DICOM_view.setBackgroundBrush(background_brush)
        self.DICOM_view.setGeometry(QtCore.QRect(0, 0, 877, 517))
        self.DICOM_view.setObjectName("DICOM_view")
        self.DICOM_view.viewport().installEventFilter(self)


    def DICOM_image_display(self):
        slider_id = self.slider.value()
        DICOM_image = self.pixmaps[slider_id]
        DICOM_image = DICOM_image.scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        DICOM_image_label = QtWidgets.QLabel()
        DICOM_image_label.setPixmap(DICOM_image)
        self.DICOM_image_scene = QtWidgets.QGraphicsScene()
        self.DICOM_image_scene.addWidget(DICOM_image_label)


    def textOnDICOM_View(self):
        # Dictionary from the dataset associated to the slice
        id = self.slider.value()
        filename = self.filepaths[id]
        dicomTreeSlice = DicomTree(filename)
        self.dictSlice = dicomTreeSlice.dict

        # Information to display
        current_slice = self.dictSlice['Instance Number'][0]
        total_slices = len(self.pixmaps)
        slice_pos = self.dictSlice['Slice Location'][0]
        row_image = self.dictSlice['Rows'][0]
        col_image = self.dictSlice['Columns'][0]
        patient_pos = self.dictSlice['Patient Position'][0]

        # For formatting
        if self.zoom == 1:
            zoom = 1
        else:
            zoom = float("{0:.2f}".format(self.zoom))

        # Add text on DICOM View
        text_imageID = QtWidgets.QGraphicsTextItem()
        text_imageID.adjustSize()
        text_imageID.setPos(QtCore.QPoint(-100, 0))
        text_imageID.setPlainText("Image: " + str(current_slice) + " / " + str(total_slices))
        text_imageID.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        text_imagePos = QtWidgets.QGraphicsTextItem()
        text_imagePos.adjustSize()
        text_imagePos.setPos(QtCore.QPoint(-100, 20))
        text_imagePos.setPlainText("Position: " + str(slice_pos) + " mm")
        text_imagePos.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        text_WL = QtWidgets.QGraphicsTextItem()
        text_WL.adjustSize()
        text_WL.setPos(QtCore.QPoint(475, 0))
        text_WL.setPlainText(f'W/L: {self.window}/{self.level}')
        text_WL.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        text_imageSize = QtWidgets.QGraphicsTextItem()
        text_imageSize.adjustSize()
        text_imageSize.setPos(QtCore.QPoint(-100, 450))
        text_imageSize.setPlainText("Image Size: " + str(row_image) + "x" + str(col_image) + "px")
        text_imageSize.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        text_zoom = QtWidgets.QGraphicsTextItem()
        text_zoom.adjustSize()
        text_zoom.setPos(QtCore.QPoint(-100, 470))
        text_zoom.setPlainText("Zoom: " + str(zoom) + ":" + str(zoom))
        text_zoom.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        text_patientPos = QtWidgets.QGraphicsTextItem()
        text_patientPos.adjustSize()
        text_patientPos.setPos(QtCore.QPoint(475, 470))
        text_patientPos.setPlainText("Position: " + patient_pos)
        text_patientPos.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        self.DICOM_image_scene.addItem(text_imageID)
        self.DICOM_image_scene.addItem(text_imagePos)
        self.DICOM_image_scene.addItem(text_WL)
        self.DICOM_image_scene.addItem(text_imageSize)
        self.DICOM_image_scene.addItem(text_patientPos)
        self.DICOM_image_scene.addItem(text_zoom)


    # When the value of the slider in the DICOM View changes
    def valueChangeSlider(self):
        self.DICOM_image_display()
        self.textOnDICOM_View()
        self.DICOM_view.setScene(self.DICOM_image_scene)
        pass

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.RightButton:
                if event.x() > self.x1:
                    self.window += 5
                elif event.x() < self.x1:
                    self.window -= 5

                if event.y() > self.y1:
                    self.level -= 5
                elif event.y() < self.y1:
                    self.level += 5

                self.x1 = event.x()
                self.y1 = event.y()

                id = self.slider.value()
                np_pixels = deepcopy(self.pixel_values[id])
                pixmap = scaled_pixmap(np_pixels, self.window, self.level)

                DICOM_image_label = QtWidgets.QLabel()
                DICOM_image_label.setPixmap(pixmap)
                DICOM_image_scene = QtWidgets.QGraphicsScene()
                DICOM_image_scene.addWidget(DICOM_image_label)
                self.DICOM_view.setScene(DICOM_image_scene)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            img_data = deepcopy(self.pixel_values)
            self.pixmaps = get_pixmaps(img_data, self.window, self.level)

        return QtCore.QObject.event(source, event)


    ###################################
    #  DICOM TREE VIEW FUNCTIONALITY  #
    ###################################

    def initTreeViewSelector(self):
        self.comboBox_TreeSelector = QtWidgets.QComboBox()
        self.comboBox_TreeSelector.setStyleSheet("QComboBox {font: 75 10pt \"Laksaman\";"
                                                 "combobox-popup: 0;"
                                                 "background-color: #efefef; }")
        self.comboBox_TreeSelector.addItem("Select a DICOM dataset...")
        self.comboBox_TreeSelector.addItem("RT Dose")
        self.comboBox_TreeSelector.addItem("RTSS")
        for i in range(len(self.pixmaps) - 1):
            self.comboBox_TreeSelector.addItem("CT Image Slice " + str(i + 1))
        self.comboBox_TreeSelector.activated.connect(self.comboTreeSelector)
        self.comboBox_TreeSelector.setFixedSize(QtCore.QSize(180, 31))
        self.vboxL_Tree.addWidget(self.comboBox_TreeSelector, QtCore.Qt.AlignLeft)


    def comboTreeSelector(self, index):
        # CT Scans
        if index > 2:
            self.updateTree(True, index - 3, "")
        # RT Dose
        elif index == 1:
            self.updateTree(False, 0, "RT Dose")
        # RTSS
        elif index == 2:
            self.updateTree(False, 0, "RTSS")

    def initTree(self):
        # Create the model for the tree
        self.modelTree = QtGui.QStandardItemModel(0, 5)
        self.modelTree.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
        self.modelTree.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
        self.modelTree.setHeaderData(2, QtCore.Qt.Horizontal, "Tag")
        self.modelTree.setHeaderData(3, QtCore.Qt.Horizontal, "VM")
        self.modelTree.setHeaderData(4, QtCore.Qt.Horizontal, "VR")
        self.treeView.setModel(self.modelTree)

    def initTreeParameters(self):
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


    def updateTree(self, ct_file, id, name):
        self.initTree()

        # The selected DICOM Dataset is a CT file
        if ct_file:
            # id is the index of the selected CT file
            filename = self.filepaths[id]
            dicomTreeSlice = DicomTree(filename)
            dict = dicomTreeSlice.dict

        # The selected DICOM Dataset is a RT Dose file
        elif name == "RT Dose":
            dict = self.dictDicomTree_rtdose

        # The selected DICOM Dataset is a RTSS file
        elif name == "RTSS":
            dict = self.dictDicomTree_rtss

        else:
            print("Error filename in updateTree function")

        parentItem = self.modelTree.invisibleRootItem()
        self.recurseBuildModel(dict, parentItem)
        self.treeView.setModel(self.modelTree)
        self.vboxL_Tree.addWidget(self.treeView)

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


    #############################
    #  TOOLBAR FUNCTI0NALITIES  #
    #############################

    def initWindowingMenu(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        for key, value in self.dict_windowing.items():
            text = str(key)
            actionWindowingItem = QtWidgets.QAction(MainWindow)
            actionWindowingItem.triggered.connect(
                lambda state, text=key: self.setWindowingLimits(state, text))
            self.menuWindowing.addAction(actionWindowingItem)
            actionWindowingItem.setText(_translate("MainWindow", text))

    def pyradiomicsHandler(self):
        self.callClass.runPyradiomics()

    def HandleAnonymization(self):
        self.callClass.runAnonymization()

    def setWindowingLimits(self, state, text):
        windowing_limits = self.dict_windowing[text]
        self.window = windowing_limits[0]
        self.level = windowing_limits[1]
        img_data = deepcopy(self.pixel_values)

        id = self.slider.value()
        np_pixels = img_data[id]
        pixmap = scaled_pixmap(np_pixels, self.window, self.level)

        DICOM_image_label = QtWidgets.QLabel()
        DICOM_image_label.setPixmap(pixmap)
        DICOM_image_scene = QtWidgets.QGraphicsScene()
        DICOM_image_scene.addWidget(DICOM_image_label)
        self.DICOM_view.setScene(DICOM_image_scene)

        self.pixmaps = get_pixmaps(img_data, self.window, self.level)

    def transectHandler(self):

        id = self.slider.value()
        dt = self.dataset[id]
        rowS = dt.PixelSpacing[0]
        colS = dt.PixelSpacing[1]
        dt.convert_pixel_data()
        self.callClass.runTransect(self.DICOM_view, self.pixmaps[id], dt._pixel_array.transpose(), rowS, colS)

    def pluginManagerHandler(self):
        self.callManager.show_plugin_manager()


import src.View.resources_rc


class HexaColor(object):
    def __init__(self):
        self.listColor = self.hexaVersionColor()

    def getHexaColor(self, index):
        return self.listColor[index][0], self.listColor[index][1], self.listColor[index][2]


    def hexaVersionColor(self):
        colors = [color.rstrip('\n') for color in open('src/View/color.txt')]
        res = []
        for color in colors:
            hex_R = self.convertHexaToDec(color[:2])
            hex_G = self.convertHexaToDec(color[2:4])
            hex_B = self.convertHexaToDec(color[-2:])
            res.append([hex_R, hex_G, hex_B])
        return res


    def convertHexaToDec(self, number):
        digit1 = self.convertHexaLetterToNumber(number[:1])
        digit2 = self.convertHexaLetterToNumber(number[-1:])
        return int(digit1) * 16 + int(digit2)


    def convertHexaLetterToNumber(self, digit):
        if digit == 'A':
            return 10
        elif digit == 'B':
            return 11
        elif digit == 'C':
            return 12
        elif digit == 'D':
            return 13
        elif digit == 'E':
            return 14
        elif digit == 'F':
            return 15
        else:
            return digit


class StructureInformation(object):
    def __init__(self, mainWindow):
        self.window = mainWindow
        self.listInfo = self.getStructInfo()

    # Return a dictionary containing volume, min, max and mean doses for all the ROIs
    def getStructInfo(self):
        res = dict()
        for id, value in self.window.rois.items():
            dvh = self.window.dvh[id]

            structInfo = dict()
            structInfo['volume'] = float("{0:.3f}".format(dvh.volume))

            # The volume of the ROI is equal to 0
            if dvh.volume == 0:
                structInfo['min'] = '-'
                structInfo['max'] = '-'
                structInfo['mean'] = '-'

            # The volume of the ROI is greater than 0
            else:
                value_DVH = 100 * dvh.counts / dvh.volume
                index = 0

                # Get the min dose of the ROI
                while value_DVH.item(index) == 100:
                    index += 1
                if index == 0:
                    structInfo['min'] = 0
                else:
                    structInfo['min'] = index-1

                # Get the max dose of the ROI
                while index < len(value_DVH) and value_DVH.item(index) > 0.01:
                    index += 1
                if index == 0:
                    structInfo['max'] = 0
                else:
                    structInfo['max'] = index-1

                # Get the mean dose of the ROI
                mean = structInfo['min'] + structInfo['max']
                structInfo['mean'] = mean/2

            res[id] = structInfo

        return res

    def getVolume(self, index):
        return self.listInfo[index]['volume']

    def getMin(self, index):
        return self.listInfo[index]['min']

    def getMax(self, index):
        return self.listInfo[index]['max']

    def getMean(self, index):
        return self.listInfo[index]['mean']



# # For Testing
# class MyWin(QtWidgets.QMainWindow):
# 	def __init__(self, parent=None):
# 		QtWidgets.QWidget.__init__(self, parent)
# 		self.ui = Ui_MainWindow()
# 		self.ui.setupUi(self, path='DicompylerDICOM')
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     myapp = MyWin()
#     myapp.show()
#     sys.exit(app.exec_())
