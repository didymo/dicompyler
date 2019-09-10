from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pylab as plt
import numpy as np
from src.Model.LoadPatients import *
from src.Model.CalculateDVHs import *
from src.Controller.mainPageController import MainPage
from matplotlib.backends.backend_qt5agg import FigureCanvas


class Ui_MainWindow(object):

    def setupUi(self, MainWindow, path, dataset, pixmaps_dict):
        self.callClass = MainPage(path, dataset, pixmaps_dict)
        self.pixmaps = pixmaps_dict

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
        self.listView_2 = QtWidgets.QListView(self.tab1_structures)
        self.listView_2.setGeometry(QtCore.QRect(0, 0, 200, 361))
        self.listView_2.setObjectName("listView_2")
        self.tab1.addTab(self.tab1_structures, "")

        # Left Column: Isodoses tab
        self.tab1_isodoses = QtWidgets.QWidget()
        self.tab1_isodoses.setObjectName("tab1_isodoses")
        self.listView = QtWidgets.QListView(self.tab1_isodoses)
        self.listView.setGeometry(QtCore.QRect(0, 0, 200, 361))
        self.listView.setObjectName("listView")
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
        self.slider.setMaximum(len(self.pixmaps)-1)
        self.slider.setValue(int(len(self.pixmaps)/2))
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
        self.gridLayout_DVH = QtWidgets.QGridLayout(self.widget_DVH)
        self.gridLayout_DVH.setObjectName("gridLayout_DVH")
        # DVH Processing
        DVH_file = getDVH(path)
        fig = DVH_view(DVH_file)
        self.plotWidget = FigureCanvas(fig)
        self.gridLayout_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)
        # DVH: Export DVH Button
        self.button_exportDVH = QtWidgets.QPushButton(self.tab2_DVH)
        self.button_exportDVH.setGeometry(QtCore.QRect(760, 358, 97, 39))
        self.button_exportDVH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportDVH.setStyleSheet("background-color: rgb(147, 112, 219);\n""color: rgb(0, 0, 0);")
        self.button_exportDVH.setObjectName("button_exportDVH")
        self.tab2.addTab(self.tab2_DVH, "")


        self.tab2.addTab(self.tab2_view, "")

        # Main view: DVH
        self.tab2_DVH = QtWidgets.QWidget()
        self.tab2_DVH.setObjectName("tab2_DVH")
        # DVH layout
        self.widget_DVH = QtWidgets.QWidget(self.tab2_DVH)
        self.widget_DVH.setGeometry(QtCore.QRect(0, 0, 877, 400))
        self.widget_DVH.setObjectName("widget_DVH")
        self.gridLayout_DVH = QtWidgets.QGridLayout(self.widget_DVH)
        self.gridLayout_DVH.setObjectName("gridLayout_DVH")

        # DVH Processing
        DVH_file = getDVH(path)
        fig = DVH_view(DVH_file)
        self.plotWidget = FigureCanvas(fig)
        self.gridLayout_DVH.addWidget(self.plotWidget, 1, 0, 1, 1)

        # DVH: Export DVH Button
        self.button_exportDVH = QtWidgets.QPushButton(self.tab2_DVH)
        self.button_exportDVH.move(15,10)
        self.button_exportDVH.setFixedSize(QtCore.QSize(100, 39))
        self.button_exportDVH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportDVH.setStyleSheet("background-color: rgb(147, 112, 219);\n""color: rgb(0, 0, 0);")
        self.button_exportDVH.setObjectName("button_exportDVH")

        self.gridLayout_DVH.addWidget(self.button_exportDVH, 1, 1, 1, 1)

        self.tab2.addTab(self.tab2_DVH, "")

        # Main view: DICOM Tree
        self.tab2_DICOM_tree = QtWidgets.QWidget()
        self.tab2_DICOM_tree.setObjectName("tab2_DICOM_tree")
        self.tableWidget = QtWidgets.QTableWidget(self.tab2_DICOM_tree)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 877, 517))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tab2.addTab(self.tab2_DICOM_tree, "")

        # Main view: Clinical Data
        self.tab2_clinical_data = QtWidgets.QWidget()
        self.tab2_clinical_data.setObjectName("tab2_clinical_data")
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
        self.widget3.setGeometry(QtCore.QRect(50, 5, 305, 31))
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
        self.widget4.setGeometry(QtCore.QRect(450, 5, 300, 31))
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

        # Menu Bar (Tools)
        self.menuROI_Creation = QtWidgets.QMenu(self.menuTools)
        self.menuROI_Creation.setObjectName("menuROI_Creation")
        self.menuExport = QtWidgets.QMenu(self.menuTools)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/Icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.menuExport.setIcon(icon9)
        self.menuExport.setObjectName("menuExport")

        # Tool Bar
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/Icon/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionZoom_In.setIcon(icon2)
        self.actionZoom_In.setIconVisibleInMenu(True)
        self.actionZoom_In.setObjectName("actionZoom_In")

        # Zoom Out Action
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/Icon/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionZoom_Out.setIcon(icon3)
        self.actionZoom_Out.setIconVisibleInMenu(True)
        self.actionZoom_Out.setObjectName("actionZoom_Out")

        # Windowing Action
        self.actionWindowing = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/Icon/windowing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionWindowing.setIcon(icon4)
        self.actionWindowing.setIconVisibleInMenu(True)
        self.actionWindowing.setObjectName("actionWindowing")

        # Transect Action
        self.actionTransect = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/Icon/transect.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionTransect.setIcon(icon5)
        self.actionTransect.setIconVisibleInMenu(True)
        self.actionTransect.setObjectName("actionTransect")

        # ROI by brush Action
        self.actionBrush = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/Icon/ROI_Brush.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionBrush.setIcon(icon6)
        self.actionBrush.setIconVisibleInMenu(True)
        self.actionBrush.setObjectName("actionBrush")

        # ROI by Isodose Action
        self.actionIsodose = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/Icon/ROI_Isodose.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionIsodose.setIcon(icon7)
        self.actionIsodose.setIconVisibleInMenu(True)
        self.actionIsodose.setObjectName("actionIsodose")

        # Plugin Manager Action
        self.actionPlugin_Manager = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/Icon/management.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionPlugin_Manager.setIcon(icon8)
        self.actionPlugin_Manager.setIconVisibleInMenu(True)
        self.actionPlugin_Manager.setObjectName("actionPlugin_Manager")

        # Anonymize and Save Action
        self.actionAnonymize_and_Save = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/Icon/save_all.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionAnonymize_and_Save.setIcon(icon1)
        self.actionAnonymize_and_Save.setIconVisibleInMenu(True)
        self.actionAnonymize_and_Save.setObjectName("actionAnonymize_and_Save")

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


        # Build toolbar
        self.menuTools.addAction(self.actionZoom_In)
        self.menuTools.addAction(self.actionZoom_Out)
        self.menuTools.addAction(self.actionWindowing)
        self.menuTools.addAction(self.actionTransect)
        self.menuTools.addAction(self.menuROI_Creation.menuAction())
        self.menuTools.addAction(self.actionPlugin_Manager)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.menuExport.menuAction())
        self.menuTools.addAction(self.actionAnonymize_and_Save)

        # Export Button on toolbar
        self.exportButton = QtWidgets.QToolButton()
        self.exportButton.setMenu(self.menuExport)
        self.exportButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.exportButton.setIcon(icon9)

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
        self.toolBar.addAction(self.actionWindowing)
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
        self.patient_DOB_box.setText(_translate("MainWindow", "01/01/90"))
        self.patient_gender_box.setText(_translate("MainWindow", "F"))
        self.patient_name_box.setText(_translate("MainWindow", "First_Name Last_Name"))
        self.patient_ID_box.setText(_translate("MainWindow", "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"))

        # Set menu labels
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
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

    def pyradiomicsHandler(self):
        self.callClass.runPyradiomics()


# In the Model directory
def getDVH(path):
    file_rtss = path + "/rtss.dcm"
    file_rtdose = path + "/rtdose.dcm"
    ds_rtss = pydicom.dcmread(file_rtss)
    ds_rtdose = pydicom.dcmread(file_rtdose)
    rois = get_roi_info(ds_rtss)
    return calc_dvhs(ds_rtss, ds_rtdose, rois)


# In the View directory
def DVH_view(dvh_file):
    fig, ax = plt.subplots()
    for roi, dvh in dvh_file.items():
        ax.plot(dvh.bincenters, 100*dvh.counts/dvh.volume, label=dvh.name,
                 color=None if not isinstance(dvh.color, np.ndarray) else
                 (dvh.color / 255))
        plt.xlabel('Dose [%s]' % dvh.dose_units)
        plt.ylabel('Volume [%s]' % '%')
        if dvh.name:
            plt.legend(loc='best')
    return fig