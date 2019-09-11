from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from src.Model.GetPatientInfo import *
from src.Model.Pyradiomics import pyradiomics
from PyQt5 import QtWidgets


class MainPage:

    def __init__(self, path):
        self.path = path

    def runPyradiomics(self):
        pyradiomics(self.path)

