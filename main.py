import sys
from src.Controller.mainPageController import *


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainPage()
    myapp.displayMainPage()
    myapp.show()
    sys.exit(app.exec_())
