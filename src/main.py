from src.Controller.mainPageController import *
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainPage()
    myapp.show()
    sys.exit(app.exec_())
