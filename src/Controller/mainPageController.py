from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox

from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from src.Model.GetPatientInfo import *
from src.Model.Pyradiomics import pyradiomics
from PyQt5 import QtWidgets
import _csv
import csv
from src.Model.form_UI import *
from src.Model.Display_CD_UI import *

message = ""


def calculate_years(year1, year2):
    return year2.year() - year1.year() - ((year2.month(), year2.day()) < (year1.month(), year1.day()))


class ClinicalDataForm(QtWidgets.QWidget, Ui_Form):
    open_patient_window = QtCore.pyqtSignal(str)

    def __init__(self, tabWindow, path):
        QtWidgets.QWidget.__init__(self)

        self.path = path
        self.tabWindow = tabWindow
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # setting tab order

        self.setTabOrder(self.ui.line_FN, self.ui.line_LN)
        self.setTabOrder(self.ui.line_FN, self.ui.date_of_birth)
        self.setTabOrder(self.ui.date_of_birth, self.ui.line_BP)
        self.setTabOrder(self.ui.line_BP, self.ui.dateEdit_2)
        self.setTabOrder(self.ui.dateEdit_2, self.ui.gender)
        self.setTabOrder(self.ui.gender, self.ui.line_icd)
        self.setTabOrder(self.ui.line_icd, self.ui.line_histology)
        self.setTabOrder(self.ui.line_histology, self.ui.T_stage)
        self.setTabOrder(self.ui.T_stage, self.ui.N_stage)
        self.setTabOrder(self.ui.N_stage, self.ui.M_stage)
        self.setTabOrder(self.ui.M_stage, self.ui.Overall_Stage)
        self.setTabOrder(self.ui.Overall_Stage, self.ui.Tx_intent)
        self.setTabOrder(self.ui.Tx_intent, self.ui.Surgery)
        self.setTabOrder(self.ui.Surgery, self.ui.Rad)
        self.setTabOrder(self.ui.Rad, self.ui.Chemo)
        self.setTabOrder(self.ui.Chemo, self.ui.Immuno)
        self.setTabOrder(self.ui.Immuno, self.ui.Branchy)
        self.setTabOrder(self.ui.Branchy, self.ui.Hormone)
        self.setTabOrder(self.ui.Hormone, self.ui.Dt_Last_Existence)
        self.setTabOrder(self.ui.Dt_Last_Existence, self.ui.Death)
        self.setTabOrder(self.ui.Death, self.ui.Cancer_death)
        self.setTabOrder(self.ui.Cancer_death, self.ui.Local_control)
        self.setTabOrder(self.ui.Local_control, self.ui.Dt_local_failure)
        self.setTabOrder(self.ui.Dt_local_failure, self.ui.Regional_Control)
        self.setTabOrder(self.ui.Regional_Control, self.ui.Dt_REgional_failure)
        self.setTabOrder(self.ui.Dt_REgional_failure, self.ui.Distant_Control)
        self.setTabOrder(self.ui.Distant_Control, self.ui.Dt_Distant_Failure)
        self.setTabOrder(self.ui.Dt_Distant_Failure, self.ui.Save_button)
        self.setTabOrder(self.ui.Save_button, self.ui.line_LN)

        self.ui.Local_control.activated.connect(self.LocalControl_Failure)
        self.ui.Regional_Control.activated.connect(self.RegionalControl_Failure)
        self.ui.Distant_Control.activated.connect(self.DistantControl_Failure)
        self.ui.Tx_intent.activated.connect(self.Tx_Intent_Refused)
        self.ui.Death.activated.connect(self.PatientDead)
        self.ui.Death.activated.connect(self.show_survival)
        self.ui.Save_button.clicked.connect(self.save_ClinicalData)

    # show survival
    def show_survival(self):
        Survival_years = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Last_Existence.date()))
        self.ui.Survival_dt.setText("Survival Length: " + Survival_years)
        self.ui.Survival_dt.setVisible(True)

    # check if patient is alive or not
    def PatientDead(self):
        status = str(self.ui.Death.currentText())
        if status == "Alive":
            self.ui.Cancer_death.setDisabled(True)
        else:
            self.ui.Cancer_death.setDisabled(False)

    # handles the case where Tx_intent is Refused
    def Tx_Intent_Refused(self):
        choice = str(self.ui.Tx_intent.currentText())
        if choice == 'Refused':
            self.ui.Surgery.setCurrentIndex(1)
            self.ui.Rad.setCurrentIndex(1)
            self.ui.Chemo.setCurrentIndex(1)
            self.ui.Immuno.setCurrentIndex(1)
            self.ui.Branchy.setCurrentIndex(1)
            self.ui.Hormone.setCurrentIndex(1)
            self.ui.Surgery.setDisabled(True)
            self.ui.Rad.setDisabled(True)
            self.ui.Chemo.setDisabled(True)
            self.ui.Immuno.setDisabled(True)
            self.ui.Branchy.setDisabled(True)
            self.ui.Hormone.setDisabled(True)
        elif choice != 'Refused':
            self.ui.Surgery.setDisabled(False)
            self.ui.Rad.setDisabled(False)
            self.ui.Chemo.setDisabled(False)
            self.ui.Immuno.setDisabled(False)
            self.ui.Branchy.setDisabled(False)
            self.ui.Hormone.setDisabled(False)
            self.ui.Surgery.setCurrentIndex(0)
            self.ui.Rad.setCurrentIndex(0)
            self.ui.Chemo.setCurrentIndex(0)
            self.ui.Immuno.setCurrentIndex(0)
            self.ui.Branchy.setCurrentIndex(0)
            self.ui.Hormone.setCurrentIndex(0)

    # get code for Surgery/Rad/Chemo/Immuno/Btrachy/Hormone
    def getCode(self, theChoice):
        if (theChoice == "Primary (Pri)"):
            return "Pri"
        elif (theChoice == "Refused (Ref)"):
            return "Ref"
        elif (theChoice == "Denied (Den)"):
            return "Den"
        elif (theChoice == "DiedB4 (Die)"):
            return "Die"
        elif (theChoice == "Neoadjuvant (Neo)"):
            return "Neo"
        elif (theChoice == "Concurrent (Con)"):
            return "Con"
        elif (theChoice == "Adjuvant (Adj)"):
            return "Adj"
        else:
            return theChoice

    # handles the change in the date of local failure according on the option selected at the local failure combo box
    def LocalControl_Failure(self):
        local_failure = str(self.ui.Local_control.currentText())
        if (local_failure == "Control"):
            self.ui.Dt_local_failure.setDisabled(True)
            # self.ui.Dt_local_failure.setReadOnly(True)
        elif (local_failure == "Failure"):
            # date = self.ui.Dt_Last_Existence.date()
            # self.ui.Dt_local_failure.setDate(date)
            self.ui.Dt_local_failure.setDisabled(False)
            self.ui.Dt_local_failure.setReadOnly(False)
        elif (local_failure == "Select..."):
            self.ui.Dt_local_failure.setDisabled(True)

    # handles the change in date of regional failure according to the regional failure option selected
    def RegionalControl_Failure(self):
        regional_failure = str(self.ui.Regional_Control.currentText())
        if (regional_failure == "Control"):
            self.ui.Dt_REgional_failure.setDisabled(True)
            # self.ui.Dt_REgional_failure.setReadOnly(False)
        elif (regional_failure == "Failure"):
            # date = self.ui.Dt_Last_Existence.date()
            # self.ui.Dt_REgional_failure.setDate(date)
            self.ui.Dt_REgional_failure.setDisabled(False)
            self.ui.Dt_REgional_failure.setReadOnly(False)
        elif (regional_failure == "Select..."):
            self.ui.Dt_REgional_failure.setDisabled(True)

    # handles the change in date of distant failure according to the option chosen in distant control
    def DistantControl_Failure(self):
        distant_failure = str(self.ui.Distant_Control.currentText())
        if (distant_failure == "Control"):
            self.ui.Dt_Distant_Failure.setDisabled(True)
            # self.ui.Dt_Distant_Failure.setReadOnly(False)
            # self.ui.Dt_Distant_Failure.setDate('')
        elif (distant_failure == "Failure"):
            # date = self.ui.Dt_Last_Existence.date()
            # self.ui.Dt_Distant_Failure.setDate(date)
            self.ui.Dt_Distant_Failure.setDisabled(False)
            self.ui.Dt_Distant_Failure.setReadOnly(False)
        elif (distant_failure == "Select..."):
            self.ui.Dt_Distant_Failure.setDisabled(True)

    # validating the data in the form
    def form_Validation(self):
        global message
        if (len(self.ui.line_LN.text()) == 0):
            message = message + "Input patient's last name. \n"
        if (len(self.ui.line_FN.text()) == 0):
            message = message + "Input patient's first name. \n"
        if (str(self.ui.gender.currentText()) == "Select..."):
            message = message + "Select patient's gender. \n"
        if (len(self.ui.line_BP.text()) == 0):
            message = message + "Input patient's birth place. \n"
        if (self.ui.date_of_birth.date() > QDate.currentDate()):
            message = message + "Patient's date of birth cannot be in the future. \n"
        if (self.ui.dateEdit_2.date() > QDate.currentDate()):
            message = message + "Patient's date of diagnosis cannot be in the future. \n"
        if (len(self.ui.line_icd.text()) == 0):
            message = message + "Input patient's ICD 10. \n"
        if (len(self.ui.line_histology.text()) == 0):
            message = message + "Input patient's Histology. \n"
        if (str(self.ui.T_stage.currentText()) == "Select..."):
            message = message + "Select patient's T Stage. \n"
        if (str(self.ui.N_stage.currentText()) == "Select..."):
            message = message + "Select patient's N Stage. \n"
        if (str(self.ui.M_stage.currentText()) == "Select..."):
            message = message + "Select patient's M Stage. \n"
        if (str(self.ui.Overall_Stage.currentText()) == "Select..."):
            message = message + "Select patient's Overall Stage. \n"
        if (str(self.ui.Tx_intent.currentText()) == "Select..."):
            message = message + "Select patient's Tx_Intent. \n"
        if (str(self.ui.Surgery.currentText()) == "Select..."):
            message = message + "Select patient's Surgery. \n"
        if (str(self.ui.Rad.currentText()) == "Select..."):
            message = message + "Select patient's Rad. \n"
        if (str(self.ui.Chemo.currentText()) == "Select..."):
            message = message + "Select patient's Chemo. \n"
        if (str(self.ui.Branchy.currentText()) == "Select..."):
            message = message + "Select patient's Brachy. \n"
        if (str(self.ui.Hormone.currentText()) == "Select..."):
            message = message + "Select patient's Hormone. \n"
        if (self.ui.Dt_Last_Existence.date() > QDate.currentDate()):
            message = message + "Patient's date of last existence cannot be in the future. \n"
        if (str(self.ui.Death.currentText()) == "Select..."):
            message = message + "Select patient's Death. \n"
        if ((str(self.ui.Cancer_death.currentText()) == "Select...") and (str(self.ui.Death.currentText()) == "Dead")):
            message = message + "Select patient's Cancer Death. \n"
        if (str(self.ui.Local_control.currentText()) == "Select..."):
            message = message + "Select patient's Local Control. \n"
        if (str(self.ui.Regional_Control.currentText()) == "Select..."):
            message = message + "Select patient's Regional Control. \n"
        if (str(self.ui.Distant_Control.currentText()) == "Select..."):
            message = message + "Select patient's Distant Control. \n"
        if (self.ui.Dt_local_failure.date() > QDate.currentDate()):
            message = message + "Patient's date of local failure cannot be in the future. \n"
        if (self.ui.Dt_REgional_failure.date() > QDate.currentDate()):
            message = message + "Patient's date of regional failure cannot be in the future. \n"
        if (self.ui.Dt_Distant_Failure.date() > QDate.currentDate()):
            message = message + "Patient's date of distant failure cannot be in the future. \n"

    # here handles the event of the button save being pressed
    def save_ClinicalData(self):
        global message
        self.form_Validation()
        if (len(message.strip()) == 0):
            # write csv file...
            new_file = os.path.join(str(self.path), 'clinicaldata.csv')
            f = open(new_file, 'w')
            columnNames = ['MD5Hash', 'Gender', 'Country_of_Birth',
                           'AgeAtDiagnosis', 'DxYear', 'Histology', 'ICD10', 'T_Stage',
                           'N_Stage', 'M_Stage', 'OverallStage', 'Tx_Intent', 'Surgery', 'Rad', 'Chemo',
                           'Immuno', 'Brachy', 'Hormone', 'Death', 'CancerDeath',
                           'Survival_Duration', 'LocalControl', 'DateOfLocalFailure', 'LC_Duration',
                           'RegionalControl', 'DateOfRegionalFailure', 'RC_Duration', 'DistantControl',
                           'DateOfDistantFailure', 'DC_Duration']
            CancerDeath = ''
            status = str(self.ui.Death.currentText())
            if status == "Dead":
                CancerDeath = str(self.ui.Cancer_death.currentText())

            ageAtDiagnosis = str(calculate_years(self.ui.date_of_birth.date(), self.ui.dateEdit_2.date()))

            # get the local failure duration
            local_failure = str(self.ui.Local_control.currentText())
            if (local_failure == "Control"):
                Lc_duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Last_Existence.date()))
                Lc_date = ''
            elif (local_failure == "Failure"):
                Lc_duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_local_failure.date()))
                Lc_date = self.ui.Dt_local_failure.date().toString("dd/MM/yyyy")

            # get the regional failure duration
            regional_failure = str(self.ui.Regional_Control.currentText())
            if (regional_failure == "Control"):
                Rc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Last_Existence.date()))
                Rc_date = ''
            elif (regional_failure == "Failure"):
                Rc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_REgional_failure.date()))
                Rc_date = self.ui.Dt_REgional_failure.date().toString("dd/MM/yyyy")

            # get the sistant failure duration
            distant_failure = str(self.ui.Distant_Control.currentText())
            if (distant_failure == "Control"):
                Dc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Last_Existence.date()))
                Dc_date = ''
            elif (distant_failure == "Failure"):
                Dc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Distant_Failure.date()))
                Dc_date = self.ui.Dt_Distant_Failure.date().toString("dd/MM/yyyy")

            Survival_years = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Last_Existence.date()))

            dataRow = ['TBD', self.ui.gender.currentText(), self.ui.line_BP.text(),
                       ageAtDiagnosis, self.ui.dateEdit_2.date().year(),
                       self.ui.line_histology.text(), self.ui.line_icd.text(), self.ui.T_stage.currentText(),
                       self.ui.N_stage.currentText(), self.ui.M_stage.currentText(),
                       self.ui.Overall_Stage.currentText(),
                       self.ui.Tx_intent.currentText(), self.getCode(self.ui.Surgery.currentText()),
                       self.getCode(self.ui.Rad.currentText()),
                       self.getCode(self.ui.Chemo.currentText()), self.getCode(self.ui.Immuno.currentText()),
                       self.getCode(self.ui.Branchy.currentText()),
                       self.getCode(self.ui.Hormone.currentText()), self.ui.Death.currentText(),
                       CancerDeath, Survival_years, self.ui.Local_control.currentText(),
                       Lc_date,
                       Lc_duration, self.ui.Regional_Control.currentText(),
                       Rc_date, Rc_Duration,
                       self.ui.Distant_Control.currentText(), Dc_date,
                       Dc_Duration]

            with f:
                writer = csv.writer(f)
                writer.writerow(columnNames)
                writer.writerow(dataRow)

            SaveReply = QMessageBox.information(self, "Message",
                                                "The Clinical Data was saved successfully in your directory!",
                                                QMessageBox.Ok)
            if SaveReply == QMessageBox.Ok:
                self.display_cd_dat()


        else:
            buttonReply = QMessageBox.warning(self, "Error Message",
                                              "The following issues need to be addressed: \n" + message, QMessageBox.Ok)
            if buttonReply == QMessageBox.Ok:
                message = ""
                pass

    def display_cd_dat(self):
        self.tab_cd = ClinicalDataDisplay(self.tabWindow,self.path)
        self.tabWindow.removeTab(3)
        self.tabWindow.addTab(self.tab_cd, "Clinical Data")
        self.tabWindow.setCurrentIndex(3)

class ClinicalDataDisplay(QtWidgets.QWidget, Ui_CD_Display):
    open_patient_window = QtCore.pyqtSignal(str)

    def __init__(self, tabWindow, path):
        QtWidgets.QWidget.__init__(self)

        self.path = path
        self.tabWindow = tabWindow
        self.ui = Ui_CD_Display()
        self.ui.setupUi(self)
        self.load_cd()
        self.ui.Edit_button.clicked.connect(self.open_form)

    def load_cd(self):
        reg = '/[clinicaldata]*[.csv]'
        pathcd = glob.glob(self.path + reg)
        clinical_data = self.load_Data(pathcd[0])

        self.ui.gender.setCurrentIndex(self.ui.gender.findText(clinical_data[1], QtCore.Qt.MatchFixedString))
        self.ui.gender.setDisabled(True)
        self.ui.line_BP.setText(clinical_data[2])
        self.ui.line_BP.setDisabled(True)
        self.ui.age_at_diagnosis.setText(clinical_data[3])
        self.ui.age_at_diagnosis.setDisabled(True)
        self.ui.line_Dx_Year.setText(clinical_data[4])
        self.ui.line_Dx_Year.setDisabled(True)
        self.ui.line_histology.setText(clinical_data[5])
        self.ui.line_histology.setDisabled(True)
        self.ui.line_icd.setText(clinical_data[6])
        self.ui.line_icd.setDisabled(True)
        self.ui.T_stage.setCurrentIndex(self.ui.T_stage.findText(clinical_data[7], QtCore.Qt.MatchFixedString))
        self.ui.T_stage.setDisabled(True)
        self.ui.N_stage.setCurrentText(clinical_data[8])
        self.ui.N_stage.setDisabled(True)
        self.ui.M_stage.setCurrentText(clinical_data[9])
        self.ui.M_stage.setDisabled(True)
        self.ui.Overall_Stage.setCurrentText(clinical_data[10])
        self.ui.Overall_Stage.setDisabled(True)
        self.ui.Tx_intent.setCurrentText(clinical_data[11])
        self.ui.Tx_intent.setDisabled(True)
        self.ui.Surgery.setCurrentText(self.getCode(clinical_data[12]))
        self.ui.Surgery.setDisabled(True)
        self.ui.Rad.setCurrentText(self.getCode(clinical_data[13]))
        self.ui.Rad.setDisabled(True)
        self.ui.Chemo.setCurrentText(self.getCode(clinical_data[14]))
        self.ui.Chemo.setDisabled(True)
        self.ui.Immuno.setCurrentText(self.getCode(clinical_data[15]))
        self.ui.Immuno.setDisabled(True)
        self.ui.Branchy.setCurrentText(self.getCode(clinical_data[16]))
        self.ui.Branchy.setDisabled(True)
        self.ui.Hormone.setCurrentText(self.getCode(clinical_data[17]))
        self.ui.Hormone.setDisabled(True)
        self.ui.Death.setCurrentText(self.getCode(clinical_data[18]))
        self.ui.Death.setDisabled(True)
        if clinical_data[19] =='':
            self.ui.Cancer_death.setCurrentIndex(-1)
        else:
            self.ui.Cancer_death.setCurrentText(self.getCode(clinical_data[19]))
        self.ui.Cancer_death.setDisabled(True)
        self.ui.survival_duration.setText(clinical_data[20])
        self.ui.survival_duration.setDisabled(True)
        self.ui.Local_control.setCurrentText(clinical_data[21])
        self.ui.Local_control.setDisabled(True)
        if clinical_data[22] == '':
            self.ui.Dt_local_failure.setDate(QtCore.QDate.fromString('01/01/1900',"dd/MM/yyyy"))
        else:
            self.ui.Dt_local_failure.setDate(QtCore.QDate.fromString(clinical_data[22], "dd/MM/yyyy"))
        self.ui.LC_duration.setText(clinical_data[23])
        self.ui.LC_duration.setDisabled(True)
        self.ui.Regional_Control.setCurrentText(clinical_data[24])
        self.ui.Regional_Control.setDisabled(True)
        if clinical_data[25] == '':
            self.ui.Dt_REgional_failure.setDate(QtCore.QDate.fromString('01/01/1900', "dd/MM/yyyy"))
        else:
            self.ui.Dt_REgional_failure.setDate(QtCore.QDate.fromString(clinical_data[25], "dd/MM/yyyy"))
        self.ui.RC_duration.setText(clinical_data[26])
        self.ui.RC_duration.setDisabled(True)
        self.ui.Distant_Control.setCurrentText(clinical_data[27])
        self.ui.Distant_Control.setDisabled(True)
        if clinical_data[28] == '':
            self.ui.Dt_Distant_Failure.setDate(QtCore.QDate.fromString('01/01/1900',"dd/MM/yyyy"))
        else:
            self.ui.Dt_Distant_Failure.setDate(QtCore.QDate.fromString(clinical_data[28], "dd/MM/yyyy"))
        self.ui.DC_duration.setText(clinical_data[29])
        self.ui.DC_duration.setDisabled(True)


    def load_Data(self,filename):
        with open(filename, 'rt')as f:
            data = csv.reader(f)
            cd = list(data)
            cd.pop(0)
            li = []
            for i in cd[0]:
                li.append(i)
            return li


    # get code for Surgery/Rad/Chemo/Immuno/Btrachy/Hormone
    def getCode(self, theChoice):
        if (theChoice == "Pri"):
            return "Primary (Pri)"
        elif (theChoice == "Ref"):
            return "Refused (Ref)"
        elif (theChoice == "Den"):
            return "Denied (Den)"
        elif (theChoice == "Die"):
            return "DiedB4 (Die)"
        elif (theChoice == "Neo"):
            return "Neoadjuvant (Neo)"
        elif (theChoice == "Con"):
            return "Concurrent (Con)"
        elif (theChoice == "Adj"):
            return "Adjuvant (Adj)"
        else:
            return theChoice

    def open_form(self):
        Reply = QMessageBox.information(self, "Message",
                                        "Option to be added soon!",
                                        QMessageBox.Ok)
        if Reply == QMessageBox.Ok:
            pass


class MainPage:

    def __init__(self, path):
        self.path = path

    def runPyradiomics(self):
        pyradiomics(self.path)

    def display_cd_form(self, tabWindow, file_path):
        self.tab_cd = ClinicalDataForm(tabWindow,file_path)
        tabWindow.addTab(self.tab_cd, "")

    def display_cd_dat(self, tabWindow, file_path):
        self.tab_cd = ClinicalDataDisplay(tabWindow,file_path)
        tabWindow.addTab(self.tab_cd, "")
