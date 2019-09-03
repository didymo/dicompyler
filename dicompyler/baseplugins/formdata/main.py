from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QMessageBox
from datetime import date

from form_UI import *
import sys

message = ""


class PopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Error Message"
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()


def calculate_years(year1, year2):
    return year2.year() - year1.year() - ((year2.month(), year2.day()) < (year1.month(), year1.day()))


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Local_control.activated.connect(self.LocalControl_Failure)
        self.ui.Regional_Control.activated.connect(self.RegionalControl_Failure)
        self.ui.Distant_Control.activated.connect(self.DistantControl_Failure)
        self.ui.Tx_intent.activated.connect(self.Tx_Intent_Refused)

        self.ui.Save_button.clicked.connect(self.save_ClinicalData)

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
            self.ui.Dt_local_failure.setDisabled(False)
            self.ui.Dt_local_failure.setReadOnly(False)
        elif (local_failure == "Failure"):
            date = self.ui.Dt_Last_Existence.date()
            self.ui.Dt_local_failure.setDate(date)
            self.ui.Dt_local_failure.setDisabled(False)
            self.ui.Dt_local_failure.setReadOnly(True)
        elif (local_failure == "Select..."):
            self.ui.Dt_local_failure.setDisabled(True)

    # handles the change in date of regional failure according to the regional failure option selected
    def RegionalControl_Failure(self):
        regional_failure = str(self.ui.Regional_Control.currentText())
        if (regional_failure == "Control"):
            self.ui.Dt_REgional_failure.setDisabled(False)
            self.ui.Dt_REgional_failure.setReadOnly(False)
        elif (regional_failure == "Failure"):
            date = self.ui.Dt_Last_Existence.date()
            self.ui.Dt_REgional_failure.setDate(date)
            self.ui.Dt_REgional_failure.setDisabled(False)
            self.ui.Dt_REgional_failure.setReadOnly(True)
        elif (regional_failure == "Select..."):
            self.ui.Dt_REgional_failure.setDisabled(True)

    # handles the change in date of distant failure according to the option chosen in distant control
    def DistantControl_Failure(self):
        distant_failure = str(self.ui.Distant_Control.currentText())
        if (distant_failure == "Control"):
            self.ui.Dt_Distant_Failure.setDisabled(False)
            self.ui.Dt_Distant_Failure.setReadOnly(False)
        elif (distant_failure == "Failure"):
            date = self.ui.Dt_Last_Existence.date()
            self.ui.Dt_Distant_Failure.setDate(date)
            self.ui.Dt_Distant_Failure.setDisabled(False)
            self.ui.Dt_Distant_Failure.setReadOnly(True)
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
        if (str(self.ui.Cancer_death.currentText()) == "Select..."):
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
            f = open('clinical_data.csv', 'w')
            columnNames = ['MD5Hash', 'Gender', 'Birth_Place',
                           'AgeAtDiagnosis', 'DxYear', 'Histology', 'ICD10', 'T_Stage',
                           'N_Stage', 'M_Stage', 'OverallStage', 'Tx_Intent', 'Surgery', 'Rad', 'Chemo',
                           'Immuno', 'Brachy', 'Hormone', 'Death', 'CancerDeath',
                           'Survival_Duration', 'LocalControl', 'DateOfLocalFailure', 'LC_Duration',
                           'RegionalControl', 'DateOfRegionalFailure', 'RC_Duration', 'DistantControl',
                           'DateOfDistantFailure', 'DC_Duration']

            ageAtDiagnosis = str(calculate_years(self.ui.date_of_birth.date(), self.ui.dateEdit_2.date()))
            Lc_duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_local_failure.date()))
            Rc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_REgional_failure.date()))
            Dc_Duration = str(calculate_years(self.ui.dateEdit_2.date(), self.ui.Dt_Distant_Failure.date()))
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
                       self.ui.Cancer_death.currentText(), Survival_years, self.ui.Local_control.currentText(),
                       self.ui.Dt_local_failure.date().toString("dd/MM/yyyy"),
                       Lc_duration, self.ui.Regional_Control.currentText(),
                       self.ui.Dt_REgional_failure.date().toString("dd/MM/yyyy"), Rc_Duration,
                       self.ui.Distant_Control.currentText(), self.ui.Dt_Distant_Failure.date().toString("dd/MM/yyyy"),
                       Dc_Duration]

            with f:
                writer = csv.writer(f)
                writer.writerow(columnNames)
                writer.writerow(dataRow)

            SaveReply = QMessageBox.information(self, "Message",
                                                "The Clinical Data was saved successfully in your directory!",
                                                QMessageBox.Ok)
            if (SaveReply == QMessageBox.Ok):
                # pass
                myapp.close()



        else:
            buttonReply = QMessageBox.warning(self, "Error Message",
                                              "The following issues need to be addressed: \n" + message, QMessageBox.Ok)
            if (buttonReply == QMessageBox.Ok):
                message = ""
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()

    sys.exit(app.exec_())
