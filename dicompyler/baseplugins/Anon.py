#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Anon.py
"""dicompyler plugin that allows Anonymise function"""
# This file is part of dicompyler, released under a BSD license.
#    See the file license.txt included with this distribution, also
#    available at https://github.com/bastula/dicompyler/
#

import logging
logger = logging.getLogger('dicompyler.quickimport')
import wx
from pubsub import pub
from dicompylercore import dicomparser
from dicompyler import util

import pydicom
import uuid
import csv
import os
import pandas as pd

def pluginProperties():
    """Properties of the plugin."""

    props = {}
    props['name'] = 'Anonymize the Identifiers'
    props['menuname'] = "&DICOM Anonymization...\tCtrl-Shift-O"
    props['description'] = "Anonymize the Identifiers "
    props['author'] = 'Augustin Pinto'
    props['version'] = "0.1.0"
    props['plugin_type'] = 'import'
    props['plugin_version'] = 1
    props['min_dicom'] = []

    return props

class plugin:

    def __init__(self, parent):

        # Initialize the import location via pubsub
        pub.subscribe(self.OnImportPrefsChange, 'general.dicom')
        pub.sendMessage('preferences.requested.values', msg='general.dicom')

        self.parent = parent

        # Setup toolbar controls
        openbmp = wx.Bitmap(util.GetResourcePath('AnonButton2.png'))
        self.tools = [{'label':"ANON", 'bmp':openbmp,
                            'shortHelp':"Anonymize the Patient Identifiers",
                            'eventhandler':self.pluginMenu}]

    def OnImportPrefsChange(self, topic, msg):
        """When the import preferences change, update the values."""
        topic = topic.split('.')
        if (topic[1] == 'import_location'):
            self.path = str(msg)
        elif (topic[1] == 'import_location_setting'):
            self.import_location_setting = msg

    def pluginMenu(self, evt):
        """Import DICOM data quickly."""

        #========================================ANONYMIZE===================================
        print("IN ANON===================")

        def hasattribute(keyword, ds):
            return keyword in ds


        ## ===================================HASH Function================================================

        def Hash_identifiers(file_no, ds_rtss):

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

            # ---------------------------sha1 hash for patient ID------------------------------

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

            # -------------------------sha1 hash for patient DOB---------------------------------------

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

            # ----------------------------sha1 hash for patient Sex------------------------------------

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
            if file_no == 1:
                if hasattribute("PatientID", ds_rtss):
                    P_name_ID = patient_name + " + " + patient_ID
                    print("Pname and ID=   ", P_name_ID)
                else:
                    P_name_ID = patient_name + " + " + "PID_empty"
                    print("Pname and ID=   ", P_name_ID)
                return (P_name_ID, hash_patient_name_sha1,1)
            else:
                return(0, hash_patient_name_sha1,0)


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
   


        # ===================================WRITE DICOM FILE================================================
        def write_hash_dcm(ds_rtss, Dicom_folder_path, file_to_write, sha1_P_name):

            Dicom_folder_path = self.path
            # Print_identifiers(ds_rtss)  # print the changed value
            # print("Writing the hash==========", sha1_P_name)
            sha1_P_name = str(sha1_P_name) # storing the hash value as a string

            print("Changing the name of file==== ",Dicom_folder_path + "/" + sha1_P_name + "_" + file_to_write)
            # save the dicom file wiith new hased identifiers
            ds_rtss.save_as(Dicom_folder_path + "/" + "Hashed" + "_" + file_to_write)
            print(":::::::Write complete :::","\n\n")

        # ====================getting all file names=================

        def get_All_files(Dicom_folder_path):

            All_dcm_fileNames = os.listdir(Dicom_folder_path)
            print("ALL files: in fuction")
            return All_dcm_fileNames


        ## ===================================PRINTING THE HASH VALUES================================================

        def Print_identifiers(ds_rtss):
            print("Patient name in dataset not hash: ", ds_rtss.PatientName)
            print("Patient ID in dataset not hash: ", ds_rtss.PatientID)
            print("Patient DOB in dataset not hash: ", ds_rtss.PatientBirthDate)
            print("Patient SEX in dataset not hash: ", ds_rtss.PatientSex)
            print("\n\n")

        ## =============loading the dicom file in the datasetc=================###

        def LOAD_DCM(Dicom_filename):
            Dicom_folder_path = self.path  # Getting and storing the Folder path of rtss.dcm file
            print("PATH of the dicom file is:-----", Dicom_folder_path)
            # creating the .dcm filename variable that we wnat to load in dataframe
            # concatinating the folder path and the filename
            Full_dicom_filepath = (Dicom_folder_path + "/" + Dicom_filename)
            print("FULL PATH of dicom file is:----", Full_dicom_filepath)
            ds_rtss = pydicom.dcmread(Full_dicom_filepath)
            # print("rtss.dcm loaded in ds_rtss")
            return ds_rtss 

        ##==========================================Anon Function==========================================
        def anon_call():
            Dicom_folder_path = self.path
           

            All_dcm = get_All_files(Dicom_folder_path)
            print("ALL files: in main ",All_dcm)

            count = 0 
            for eachFile in All_dcm:
                count +=1
                print("HASHING FILE === ",eachFile)
                Dicom_filename = eachFile       # store the name of each dcm file in variable
                # concatinating the folder path and the filename
                Full_dicom_filepath = (Dicom_folder_path + "/" + Dicom_filename)

                ds_rtss = LOAD_DCM(Dicom_filename)  # readind the DCM FILE
                print(" loaded in ds_rtss:============ ", Dicom_filename)

                # calling the HASH function and it returns the (Pname + PID), (hashvalue) and
                # (flag = 1 that will be used to restrict only one hash per patient in the CSV file)
                pname_ID, sha1_pname, flag = Hash_identifiers(count, ds_rtss)
                

                if flag == 1:   #(flag = 1 that will be used to restrict only one hash per patient in the CSV file)
                    # print("FLAG --1111111111111111111111111\n")
                    print(" In main Pname and ID=  {} and SHA1_name: {}".format(pname_ID, sha1_pname))
                    Print_identifiers(ds_rtss)  # calling the print to show the identifiers
                    print("========File used for CSV export :::", Dicom_filename)
                    csv_filename = str("Hash_map") + ".csv"
                    create_hash_csv(pname_ID, sha1_pname, csv_filename) # calling create CSV to store the the hashed value
                    print("Calling WRITE FUNCTION==============")
                    # write_hash_dcm(sha1_pname, Dicom_filename)
                    write_hash_dcm(ds_rtss, Dicom_folder_path , Dicom_filename, sha1_pname)
                else:
                    # print("FLAG --0000000000000000000000000\n")
                    print("CSV function not called")
                    print("Calling WRITE FUNCTION==============")
                    # write_hash_dcm(sha1_pname, Dicom_filename)
                    write_hash_dcm(ds_rtss, Dicom_folder_path , Dicom_filename, sha1_pname)
            
            print("Total files hashed======", count)



        # Calling Anonymization
        anon_call()

        return




