from src.View.mainPage import *


from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from PyQt5 import QtWidgets



class MainPage(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainPage, self).__init__(parent=parent)
        self.path=''
        self.dataset = []
        self.pixmaps = []



    def displayMainPage(self):
        QtWidgets.QWidget.__init__(self)
        #self.hide()
        #self.show()
       # print("show 1")

        self.ui = Ui_MainWindow()
       # self.hide()
        self.ui.setupUi(self, self.pixmaps, self.path)
        self.show()
        #self.close()
        # self.refresh()        #self.show()
        print("show 2")
        #self.hide()



    def openPatient(self):
       # QtWidgets.QWidget.__init__(self)
        # self.hide()
        self.path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select patient folder...')
        #self.hide()
        self.dataset = get_datasets(self.path)
        self.pixmaps = get_pixmaps(self.dataset)

        self.displayMainPage()
        #self.show()
        print(self.path)