


#### THE Anonimization function for the patient identifiers #########
 
import os
import pydicom
import uuid
import csv
import pandas as pd

#========================================ANONYMIZation code ===================================


# CHECK if the identifiers exist in dicom file
def hasattribute(keyword, ds):
    return keyword in ds

# ## ===================================PRINTING THE HASH VALUES================================================

def Print_identifiers(ds_rtss):
    print("INSIDE PRINT================")
    print("Patient name in dataset not hash: ", ds_rtss.PatientName)
    print("Patient ID in dataset not hash: ", ds_rtss.PatientID)
    print("Patient DOB in dataset not hash: ", ds_rtss.PatientBirthDate)
    print("Patient SEX in dataset not hash: ", ds_rtss.PatientSex)
    print("\n\n")


# loading the dicom file 
def LOAD_DCM(Dicom_folder_path):
    # Dicom_folder_path = self.path  # Getting and storing the Folder path of rtss.dcm file
    print("PATH of the dicom file is:-----", Dicom_folder_path, "\n\n")
    # creating the .dcm filename variable that we wnat to load in dataframe
    Dicom_filename = "rtss.dcm"
    # concatinating the folder path and the filename
    Full_dicom_filepath = (Dicom_folder_path + "/" + Dicom_filename)
    print("FULL PATH of dicom file is:----", Full_dicom_filepath)
    ds_rtss = pydicom.dcmread(Full_dicom_filepath)
    print("rtss.dcm loaded in ds_rtss")
    return ds_rtss

## ===================================HASH Function================================================
def Hash_identifiers(ds_rtss):

    # ------------------------------------Sha1 hash for patient name-------------------------------------

    if 'PatientName' in ds_rtss:
        patient_name = str(ds_rtss.PatientName)
        print("Patient name - ", patient_name)
        # MD 5 hashing
        hash_patient_name_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_name)
        # Hashing the MD5 haah again using SHA1
        hash_patient_name_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_name_MD5))
        # storing the hash to dataset
        ds_rtss.PatientName = str(hash_patient_name_sha1)
        print("\n\n")
    else:
        print("NO patient Name found")

    # -----------------------------------------sha1 hash for patient ID------------------------------

    # if 'PatientID' in ds_rtss:
    if hasattribute("PatientID", ds_rtss):
        patient_ID = str(ds_rtss.PatientID)
        print("Patient ID - ", patient_ID)
        # MD 5 hashing
        hash_patient_ID_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_ID)
        # Hashing the MD5 haah again using SHA1
        hash_patient_ID_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_ID_MD5))
        # storing the hash to dataset
        ds_rtss.PatientID = str(hash_patient_ID_sha1)
        print("\n\n")
    else:
        print("NO patient ID not found")

    #  storing patient_name and ID in one variable
    if hasattribute("PatientID", ds_rtss):
        P_name_ID = patient_name + " + " + patient_ID
    else:
        P_name_ID = patient_name + " + " + "PID_empty"

    # print("\n\n")
    # ----------------------------------------------sha1 hash for patient DOB---------------------------------------

    if 'PatientBirthDate' in ds_rtss:
        patient_DOB = str(ds_rtss.PatientBirthDate)
        print("Patient DOB - ", patient_DOB)
        # MD 5 hashing
        hash_patient_DOB_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_DOB)
        # Hashing the MD5 haah again using SHA1
        hash_patient_DOB_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_DOB_MD5))
        # storing the hash to dataset
        ds_rtss.PatientBirthDate = str(hash_patient_DOB_sha1)
        print("\n\n")
    else:
        print("Patient BirthDate not found")

    # --------------------------------------------sha1 hash for patient Sex------------------------------------

    if 'PatientSex' in ds_rtss:
        patient_sex = str(ds_rtss.PatientSex)
        print("Patient Sex - ", patient_sex)
        # MD 5 hashing
        hash_patient_Sex_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_sex)
        # Hashing the MD5 haah again using SHA1
        hash_patient_Sex_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_Sex_MD5))
        # storing the hash to dataset
        ds_rtss.PatientSex = str(hash_patient_Sex_sha1)
        print('\n\n')
    else:
        print("Patient Sex not found")

    return (P_name_ID, hash_patient_name_sha1)



 ## ===================================CHECK FILE EXIST================================================

def checkFileExist(fileName):
    print("file name:-- ", fileName)  # printing file name

    if (fileName == "Hash_map.csv"):
        cwd = os.getcwd()  # getting the current working directory
        file_path = cwd + "/" + fileName  # concatenating the current working directory with the csv filename
        print("Full path :  ===========", file_path)  # print the full csv file path
        print("file exist: ", os.path.isfile(file_path))  # check if the file exist in the folder
        if (os.path.isfile(file_path)) == True:  # if file exist return True
            print("returning true-----------------------")
            return True
        else:
            print("returning false----------------------")  # if file not exist return false
            return False    


 ## ===================================CTEATE CSV FILE================================================

def create_hash_csv(pname, sha1_pname, csv_filename):

    # print("Csv file name is : ",csv_filename)
    # csv_filename = str("Hash_map") + ".csv"
    if (checkFileExist(csv_filename)) == False:
        print("-----Creating CSV------")

        csv_header = []
        csv_header.append('Pname and ID')
        csv_header.append('Hashed_Pname')
        print("the headers are:--", csv_header)

        # hash_dictionary =  {patient_ID : hash_patient_ID}
        # print("dictionary values",hash_dictionary)

        df_identifier_csv = pd.DataFrame(columns=csv_header).round(2)
        df_identifier_csv.to_csv(csv_filename, index=False) # creating the CVS

        row = [pname, sha1_pname]
        with open(csv_filename, 'a') as csvFile:  # inserting the hash values
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()

        # print("The dataframe",df_identifier_csv)
        print("---------CSV created-----------")
        # options()

    else:
        print("updating csv")
        row = [pname, sha1_pname]
        with open(csv_filename, 'a') as csvFile: # updating the CVS with hash values
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
        print("------CSV updated -----")


# ===================================Writing the hashed identifiers to DICOM FILE================================================
def write_hash_dcm(sha1_P_name, ds_rtss, Dicom_folder_path):

    Print_identifiers(ds_rtss)  # print the changed value
    print("Writing the hash==========", sha1_P_name)
    sha1_P_name = str(sha1_P_name)

    print("Changing the name of file==== ",Dicom_folder_path + "/" + sha1_P_name + "_" + "rtss.dcm")
    ds_rtss.save_as(Dicom_folder_path + "/" + sha1_P_name + "_" + "rtss.dcm")
    print(":::::::Write complete :::")


# ##==========================================Anon Function==========================================
def anon_call(path):
    Dicom_folder_path = path
    ds_rtss= LOAD_DCM(path)
    Print_identifiers(ds_rtss)
    pname_ID, sha1_pname = Hash_identifiers(ds_rtss)
    print(" In main Pname and ID=  {} and SHA1_name: {}".format(pname_ID, sha1_pname))
    csv_filename = str("Hash_map") + ".csv"
    create_hash_csv(pname_ID, sha1_pname, csv_filename)
    print("Calling WRITE FUNCTION==============")
    write_hash_dcm(sha1_pname, ds_rtss, Dicom_folder_path)


def anonymize(path):

    print("   Current Work Directory is:  ==== ",os.getcwd())
    print("IN ANON===================")
    print("Path in Anon   ===",path)
    anon_call(path)

