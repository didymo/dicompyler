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

        # Import rtss.dcm. Only rtss is related to the ROI info, according to my research so far.

        ds_rtss = pydicom.dcmread("rtss.dcm")
        print("rtss.dcm loaded in ds_rtss")
        patient_ID = str(ds_rtss.PatientID)
        hash_patient_ID = str(uuid.uuid3(uuid.NAMESPACE_URL, patient_ID))
        # print("printing hash",hash_patient_ID)


        # ---------- This is for hashlib  Tried Ignore --------
        # m = hashlib.sha256()
        # u = unicode(patient_name, "utf-8")
        # obj = str(patient_name).encode('utf8')
        # hash_Pname = m.update(patient_name)
        # m.digest()
        # print("Hashlib Pname: ---- ",hash_Pname)
        # print("Printingn dataset - ",ds_rtss)
        # ----------------------------------


        # Function to Hash Patient Name , ID , Sex , Date-0f-birth
        def Hash_identifiers():
            # ------------------------------------Sha1 hash for patient name-------------------------------------
            if 'PatientName' in ds_rtss:
                patient_name = str(ds_rtss.PatientName)

                print("Patient name - ", patient_name)

                hash_patient_name = uuid.uuid3(uuid.NAMESPACE_URL, patient_name)
                print("Hash value for patient name : ", hash_patient_name)
                # ds_rtss.patientName = hash_patient_name
                ds_rtss.PatientName = str(hash_patient_name)
                print("Class of Patientname is: ", type(ds_rtss.PatientName))
                print("Hash changed in dataset for patient name:---- ", ds_rtss.PatientName)
                # print(" hash changed in Dataset for patient name: ",ds_rtss.Patientname)
                # print("The SHA1 hash for patient name variable  is  : ",hash_patient_name)   # uuid.uuid3(uuid.NAMESPACE_URL, patient_name)
                # print("Patient Name: " + str(ds_rtss.Patientname),'\n\n')
                print("\n\n")
            else:
                print("NO patient Name found")

            # -----------------------------------------sha1 hash for patient ID------------------------------

            # if 'PatientID' in ds_rtss:
            if hasattribute("PatientID", ds_rtss):
                patient_ID = str(ds_rtss.PatientID)
                print("Patient ID - ", patient_ID)

                hash_patient_ID = uuid.uuid3(uuid.NAMESPACE_URL, patient_ID)
                ds_rtss.PatientID = str(hash_patient_ID)
                print("Class of Patientid is: ", type(ds_rtss.PatientID))
                print(" hash changed in Dataset for patient ID: ", ds_rtss.PatientID)
                # print("The SHA1 hash for patient ID variable is  : ",hash_patient_ID)       #uuid.uuid3(uuid.NAMESPACE_URL, patient_ID))
                print("Patient ID: " + str(ds_rtss.PatientID), '\n\n')
            else:
                print("NO patient ID not found")

            # ----------------------------------------------sha1 hash for patient DOB---------------------------------------

            if 'PatientBirthDate' in ds_rtss:
                patient_DOB = str(ds_rtss.PatientBirthDate)
                print("Patient DOB - ", patient_DOB)
                hash_patient_DOB = uuid.uuid3(uuid.NAMESPACE_URL, patient_DOB)
                ds_rtss.PatientBirthDate = str(hash_patient_DOB)
                print("Class of DOB is: ", type(ds_rtss.PatientBirthDate))
                print(" The hash changed in Dataset for patient DOB: ", ds_rtss.PatientBirthDate)
                # print("The SHA1 hash for patient DOB is :",hash_patient_DOB)        # uuid.uuid3(uuid.NAMESPACE_URL,patient_DOB)
                print("Patient Birth Date: " + str(ds_rtss.PatientBirthDate), '\n\n')
            else:
                print("Patient BirthDate not found")

            # --------------------------------------------sha1 hash for patient Sex------------------------------------

            if 'PatientSex' in ds_rtss:
                patient_sex = str(ds_rtss.PatientSex)
                print("Patient Sex - ", patient_sex)
                hash_patient_Sex = uuid.uuid3(uuid.NAMESPACE_URL, patient_sex)
                ds_rtss.PatientSex = str(hash_patient_Sex)
                print("Class of Sex is: ", type(ds_rtss.PatientSex))
                print("hash changed in Dataset for patient sex: ", ds_rtss.PatientSex)
                # print("The SHA1 hash for patient SEX is :",hash_patient_Sex)     #uuid.uuid3(uuid.NAMESPACE_URL,patient_sex))
                print("Patient Sex: " + str(ds_rtss.PatientSex) + '\n')
            else:
                print("Patient Sex not found")

            # Call options again for the user
            # options()


       ### OPTION USED JUSTED FOR TESTING IGNORE
        def options():
            print("\nPLease specify the task by selecting from OPTIONS:--\n\n")
            print("----OPTIONS----\n")
            print(" 1. Hash the identifiers\n", "2. Create Hashed CSV\n", "3. Exit \n")
            action = int(input("Select the task (1 or 2 or 3) ::: value:-- \n"))
            if (action == 1):
                print("hashing identifiers")
                Hash_identifiers()
                # patient_ID,patient_ID_hash = Hash_identifiers()
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
        Hash_identifiers()
        print("=========FINISHED HASHING in SHAI")










        # dlg = wx.FileDialog(
        #     self.parent, defaultDir=self.path,
        #     wildcard="All Files (*.*)|*.*|DICOM File (*.dcm)|*.dcm",
        #     message="Choose to ANON")
        #
        # patient = {}
        # if dlg.ShowModal() == wx.ID_OK:
        #     filename = dlg.GetPath()
        #     # Try to parse the file if is a DICOM file
        #     try:
        #         logger.debug("Reading: %s", filename)
        #         dp = dicomparser.DicomParser(filename)
        #     # Otherwise show an error dialog
        #     except (AttributeError, EOFError, IOError, KeyError):
        #         logger.info("%s is not a valid DICOM file.", filename)
        #         dlg = wx.MessageDialog(
        #             self.parent, filename + " is not a valid DICOM file.",
        #             "Invalid DICOM File", wx.OK | wx.ICON_ERROR)
        #         dlg.ShowModal()
        #     # If this is really a DICOM file, place it in the appropriate bin
        #     else:
        #         if (('ImageOrientationPatient' in dp.ds) and not (dp.ds.Modality in ['RTDOSE'])):
        #             patient['images'] = []
        #             patient['images'].append(dp.ds)
        #         elif (dp.ds.Modality in ['RTSTRUCT']):
        #             patient['rtss'] = dp.ds
        #         elif (dp.ds.Modality in ['RTPLAN']):
        #             patient['rtplan'] = dp.ds
        #         elif (dp.ds.Modality in ['RTDOSE']):
        #             patient['rtdose'] = dp.ds
        #         else:
        #             patient[dp.ds.Modality] = dp.ds
        #         # Since we have decided to use this location to import from,
        #         # update the location in the preferences for the next session
        #         # if the 'import_location_setting' is "Remember Last Used"
        #         if (self.import_location_setting == "Remember Last Used"):
        #             pub.sendMessage('preferences.updated.value',
        #                             msg={'general.dicom.import_location': dlg.GetDirectory()})
        #             pub.sendMessage('preferences.requested.values', msg='general.dicom')
        # pub.sendMessage('patient.updated.raw_data', msg=patient)
        # dlg.Destroy()
        # return




