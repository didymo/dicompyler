from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from src.Model.Pyradiomics import pyradiomics
from PyQt5 import QtWidgets


class MainPage:

    def __init__(self, path, pixmaps, dataset):
        self.path = path
        self.dataset = dataset
        self.pixmaps = pixmaps


    def runPyradiomics(self):
        pyradiomics(self.path)

