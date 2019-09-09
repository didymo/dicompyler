#!/usr/bin/env python
# -*- coding: utf-8 -*-
# quickopen.py
"""dicompyler plugin that allows quick import of DICOM data."""
# Copyright (c) 2012-2017 Aditya Panchal
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
    props['name'] = 'DICOM Quick Import'
    props['menuname'] = "&DICOM File Quickly...\tCtrl-Shift-O"
    props['description'] = "Import DICOM data quickly"
    props['author'] = 'Aditya Panchal'
    props['version'] = "0.5.0"
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
        openbmp = wx.Bitmap(util.GetResourcePath('folder_image.png'))
        self.tools = [{'label':"ANON", 'bmp':openbmp,
                            'shortHelp':"Open DICOM File Quickly...",
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

        Dicom_folder_path = self.path  # Getting and storing the Folder path of rtss.dcm file
        print("PATH of the dicom file is:-----", Dicom_folder_path, "\n\n")
        # creating the .dcm filename variable that we wnat to load in dataframe
        Dicom_filename = "rtss.dcm"
        # concatinating the folder path and the filename
        Full_dicom_filepath = (Dicom_folder_path + "/" + Dicom_filename)
        print("FULL PATH of dicom file is:----", Full_dicom_filepath)
        ds_rtss = pydicom.dcmread(Full_dicom_filepath)
        print("rtss.dcm loaded in ds_rtss")


        ## ===================================HASH Function================================================
        def Hash_identifiers():

            # ------------------------------------Sha1 hash for patient name-------------------------------------

            if 'PatientName' in ds_rtss:
                patient_name = str(ds_rtss.PatientName)
                print("Patient name - ", patient_name)

                hash_patient_name_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_name)
                print("MD5 patient name:----", hash_patient_name_MD5)
                hash_patient_name_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_name_MD5))
                print("Sha1 patient name:----", hash_patient_name_sha1)
                ds_rtss.PatientName = str(hash_patient_name_sha1)
                print("Class of Patientname is: ", type(ds_rtss.PatientName))
                print("Hash changed in dataset for patient name:---- ", ds_rtss.PatientName)

                print("\n\n")
            else:
                print("NO patient Name found")

            # -----------------------------------------sha1 hash for patient ID------------------------------

            # if 'PatientID' in ds_rtss:
            if hasattribute("PatientID", ds_rtss):
                patient_ID = str(ds_rtss.PatientID)
                print("Patient ID - ", patient_ID)

                hash_patient_ID_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_ID)
                print("MD5 patient ID:----", hash_patient_ID_MD5)
                hash_patient_ID_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_ID_MD5))
                print("Sha1 patient ID:----", hash_patient_ID_sha1)
                ds_rtss.PatientID = str(hash_patient_ID_sha1)
                print("Class of PatientID is: ", type(ds_rtss.PatientID))
                print("Hash changed in Dataset for patient ID: ", ds_rtss.PatientID)
                print("\n\n")
            else:
                print("NO patient ID not found")

            #  storing patient_name and ID in one variable
            if hasattribute("PatientID", ds_rtss):
                P_name_ID = patient_name + " + " + patient_ID
                print("Pname and ID=   ", P_name_ID)
            else:
                P_name_ID = patient_name + " + " + "PID_empty"
                print("Pname and ID=   ", P_name_ID)

            print("\n\n")
            # ----------------------------------------------sha1 hash for patient DOB---------------------------------------

            if 'PatientBirthDate' in ds_rtss:
                patient_DOB = str(ds_rtss.PatientBirthDate)
                print("Patient DOB - ", patient_DOB)

                hash_patient_DOB_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_DOB)
                print("MD5 patient DOB:----", hash_patient_DOB_MD5)
                hash_patient_DOB_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_DOB_MD5))
                print("Sha1 patient DOB:----", hash_patient_DOB_sha1)
                ds_rtss.PatientBirthDate = str(hash_patient_DOB_sha1)
                print("Class of DOB is: ", type(ds_rtss.PatientBirthDate))
                print("Hash changed in Dataset for patient DOB: ", ds_rtss.PatientBirthDate)
                print("\n\n")
            else:
                print("Patient BirthDate not found")

            # --------------------------------------------sha1 hash for patient Sex------------------------------------

            if 'PatientSex' in ds_rtss:
                patient_sex = str(ds_rtss.PatientSex)
                print("Patient Sex - ", patient_sex)

                hash_patient_Sex_MD5 = uuid.uuid5(uuid.NAMESPACE_URL, patient_sex)
                print("MD5 patient SEX:----", hash_patient_Sex_MD5)
                hash_patient_Sex_sha1 = uuid.uuid3(uuid.NAMESPACE_URL, str(hash_patient_Sex_MD5))
                print("Sha1 patient SEX:----", hash_patient_Sex_sha1)
                ds_rtss.PatientSex = str(hash_patient_Sex_sha1)
                print("Class of Sex is: ", type(ds_rtss.PatientSex))
                print("hash changed in Dataset for patient sex: ", ds_rtss.PatientSex)
                print('\n\n')
            else:
                print("Patient Sex not found")

            return (P_name_ID, hash_patient_name_sha1)
            # Call options again for the user
            # options()

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
                df_identifier_csv.to_csv(csv_filename, index=False)

                row = [pname, sha1_pname]
                with open(csv_filename, 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                    csvFile.close()

                # print("The dataframe",df_identifier_csv)
                print("---------CSV created-----------")
                # options()

            else:
                print("updating csv")
                row = [pname, sha1_pname]
                with open(csv_filename, 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                    csvFile.close()
                print("------CSV updated -----")
                # options()

        def options():
            print("\nPLease specify the task by selecting from OPTIONS:--\n\n")
            print("----OPTIONS----\n")
            print(" 1. Hash the identifiers\n", "2. Create Hashed CSV\n", "3. Exit \n")
            action = int(input("Select the task (1 or 2 or 3) ::: value:-- \n"))
            if (action == 1):
                print("hashing identifiers")
                Hash_identifiers()
                # options()
            if (action == 2):
                print("creating or updation CSV")
                create_hash_csv()
            if (action == 3):
                exit(0)


        ## ===================================PRINTING THE HASH VALUES================================================

        def Print_identifiers():
            print("Patient name in dataset not hash: ", ds_rtss.PatientName)
            print("Patient ID in dataset not hash: ", ds_rtss.PatientID)
            print("Patient DOB in dataset not hash: ", ds_rtss.PatientBirthDate)
            print("Patient SEX in dataset not hash: ", ds_rtss.PatientSex)
            print("\n\n")

        ##==========================================CALLING HASHING ==========================================    

        Print_identifiers()
        pname_ID, sha1_pname = Hash_identifiers()
        print(" In main Pname and ID=  {} and SHA1_name: {}".format(pname_ID, sha1_pname))
        csv_filename = str("Hash_map") + ".csv"
        create_hash_csv(pname_ID, sha1_pname, csv_filename)

        return




