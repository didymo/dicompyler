import sys
from src.View.PluginManager import *

class PluginManager(QtWidgets.QMainWindow, Ui_PluginManager):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

class PManager:

    def __init__(self):
        pass

    def show_plugin_manager(self):
        self.plugin_window = PluginManager()
        self.plugin_window.show()