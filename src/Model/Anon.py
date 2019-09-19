


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



## ===================================HASH Function================================================

def Hash_identifiers(file_to_write, ds_rtss):

    # ------------------------------------Sha1 hash for patient name-------------------------------------

    if 'PatientName' in ds_rtss:
        patient_name = str(ds_rtss.PatientName)
        # print("Patient name - ", patient_name)
        # MD 5 hashing
        hash_patient_name_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_name)
        # Hashing the MD5 hash again using SHA1
        hash_patient_name_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_name_MD5))
        # storing the hash to dataset
        ds_rtss.PatientName = str(hash_patient_name_sha1)
    else:
        print("NO patient Name found")

    # -----------------------------------------sha1 hash for patient ID------------------------------

    # if 'PatientID' in ds_rtss:
    if hasattribute("PatientID", ds_rtss):
        patient_ID = str(ds_rtss.PatientID)
        # print("Patient ID - ", patient_ID)
        # MD 5 hashing
        hash_patient_ID_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_ID)
        # Hashing the MD5 hash again using SHA1
        hash_patient_ID_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_ID_MD5))
        # storing the hash to dataset
        ds_rtss.PatientID = str(hash_patient_ID_sha1)
    else:
        print("NO patient ID not found")

    # #  storing patient_name and ID in one variable
    # if hasattribute("PatientID", ds_rtss):
    #     P_name_ID = patient_name + " + " + patient_ID
    # else:
    #     P_name_ID = patient_name + " + " + "PID_empty"

    # ----------------------------------------------sha1 hash for patient DOB---------------------------------------

    if 'PatientBirthDate' in ds_rtss:
        patient_DOB = str(ds_rtss.PatientBirthDate)
        # print("Patient DOB - ", patient_DOB)
        # MD 5 hashing
        hash_patient_DOB_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_DOB)
        # Hashing the MD5 hash again using SHA1
        hash_patient_DOB_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_DOB_MD5))
        # storing the hash to dataset
        ds_rtss.PatientBirthDate = str(hash_patient_DOB_sha1)
    else:
        print("Patient BirthDate not found")

    # --------------------------------------------sha1 hash for patient Sex------------------------------------

    if 'PatientSex' in ds_rtss:
        patient_sex = str(ds_rtss.PatientSex)
        # print("Patient Sex - ", patient_sex)
        # MD 5 hashing
        hash_patient_Sex_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_sex)
        # Hashing the MD5 hash again using SHA1
        hash_patient_Sex_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_Sex_MD5))
        # storing the hash to dataset
        ds_rtss.PatientSex = str(hash_patient_Sex_sha1)
    else:
        print("Patient Sex not found")


     # used to reture flag = 1 to indicate the first file is used for saving the hash in 
     # hash_CSV file so CSV function will not be performed for rest of the files.   
    if file_to_write == "rtss.dcm":
        if hasattribute("PatientID", ds_rtss):
            P_name_ID = patient_name + " + " + patient_ID
            print("Pname and ID=   ", P_name_ID)
        else:
            P_name_ID = patient_name + " + " + "PID_empty"
            print("Pname and ID=   ", P_name_ID)
        return (P_name_ID, hash_patient_name_sha1,1)
    else:
        return(0,0,0)



 ## ===================================CHECK FILE EXIST================================================

def checkFileExist(fileName, Dicom_folder_path):
    print("file name:-- ", fileName)  # printing file name

    if (fileName == "Hash_map.csv"):
        # cwd = os.getcwd()  # getting the current working directory
        file_path = Dicom_folder_path + "/" + fileName  # concatenating the current working directory with the csv filename
        print("Full path :  ===========", file_path)  # print the full csv file path
        print("file exist: ", os.path.isfile(file_path))  # check if the file exist in the folder
        if (os.path.isfile(file_path)) == True:  # if file exist return True
            print("returning true-----------------------")
            return True
        else:
            print("returning false----------------------")  # if file not exist return false
            return False    


 ## ===================================CTEATE CSV FILE================================================

def create_hash_csv(pname, sha1_pname, csv_filename, Dicom_folder_path):

    # concatinating the filename and the path of patient folder.
    csv_file_path = Dicom_folder_path + "/" + csv_filename
    print("Csv file name is : ",csv_file_path)
    # csv_filename = str("Hash_map") + ".csv"

    if (checkFileExist(csv_filename, Dicom_folder_path)) == False:
        print("-----Creating CSV------")

        #creating the headers for the CSV file
        csv_header = []
        csv_header.append('Pname and ID')
        csv_header.append('Hashed_Pname')
        print("the headers are:--", csv_header)

        # hash_dictionary =  {patient_ID : hash_patient_ID}
        # print("dictionary values",hash_dictionary)

        df_identifier_csv = pd.DataFrame(columns=csv_header).round(2)
        df_identifier_csv.to_csv(csv_file_path, index=False) # creating the CSV

        row = [pname, sha1_pname]
        with open(csv_file_path, 'a') as csvFile:  # inserting the hash values
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()

        # print("The dataframe",df_identifier_csv)
        print("---------CSV created-----------")
        # options()

    else:
        print("updating csv")
        row = [pname, sha1_pname]
        with open(csv_file_path, 'a') as csvFile: # updating the CVS with hash values
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


# ===============================getting all file names================

def get_All_files(Dicom_folder_path):

    All_dcm_fileNames = os.listdir(Dicom_folder_path)
    print("ALL files: in fuction")
    return All_dcm_fileNames

# ## ===================================PRINTING THE HASH VALUES================================================

def Print_identifiers(ds_rtss):
    print("INSIDE PRINT================")
    print("Patient name in dataset not hash: ", ds_rtss.PatientName)
    print("Patient ID in dataset not hash: ", ds_rtss.PatientID)
    print("Patient DOB in dataset not hash: ", ds_rtss.PatientBirthDate)
    print("Patient SEX in dataset not hash: ", ds_rtss.PatientSex)
    print("\n\n")


# loading the dicom file 
def LOAD_DCM(Dicom_folder_path,Dicom_filename):
    # Dicom_folder_path = self.path  # Getting and storing the Folder path of rtss.dcm file
    print("PATH of the dicom file is:-----", Dicom_folder_path)

    # concatinating the folder path and the filename
    Full_dicom_filepath = (Dicom_folder_path + "/" + Dicom_filename)
    print("FULL PATH of dicom file is:----", Full_dicom_filepath)
    ds_rtss = pydicom.dcmread(Full_dicom_filepath)
    print("rtss.dcm loaded in ds_rtss")
    return ds_rtss

# ##==========================================Anon Function==========================================
def anon_call(path):
    
    Dicom_folder_path = path

    All_dcm = get_All_files(Dicom_folder_path)
    print("ALL files: in main ")

    count = 0 
    for eachFile in All_dcm:
        count += 1

        Dicom_filename = eachFile       # store the name of each dcm file in a variable
        print("HASHING FILE === ",Dicom_filename)

        # loading the dicom file content into the dataframe.
        ds_rtss= LOAD_DCM(Dicom_folder_path,Dicom_filename)
        print("loaded in ds_rtss:============ ", Dicom_filename)

        # calling the HASH function and it returns the (Pname + PID), (hashvalue) and
        # (flag = 1  will be used to restrict only one hash value per patient in the CSV file)
        pname_ID, sha1_pname, flag = Hash_identifiers(Dicom_filename, ds_rtss)

        if flag == 1:   #(flag = 1 that will be used to restrict only one hash per patient in the CSV file)
            print("FLAG --1111111111111111111111111\n")
            print(" In main Pname and ID=  {} and SHA1_name: {}".format(pname_ID, sha1_pname))

            Print_identifiers(ds_rtss)  # calling the print to show the identifiers
            csv_filename = str("Hash_map") + ".csv"
            # calling create CSV to store the the hashed value
            create_hash_csv(pname_ID, sha1_pname, csv_filename, Dicom_folder_path)
        else:
            print("FLAG --0000000000000000000000000\n")
            print("CSV function not called")
            

    print("Total files hashed======", count)


def anonymize(path):

    print("   Current Work Directory is:  ==== ",os.getcwd())
    print("IN ANON===================")
    print("Path in Anon   ===",path)
    anon_call(path)


