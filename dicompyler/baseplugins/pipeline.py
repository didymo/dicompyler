#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pipeline.py

"""dicompyler plugin that allows pyradiomics analysis"""

# This file is part of dicompyler, released under a BSD license.
#    See the file license.txt included with this distribution, also
#    available at https://github.com/bastula/dicompyler/

import logging
logger = logging.getLogger('dicompyler.pipeline')
import wx
import os
from pubsub import pub
from dicompylercore import dicomparser
from dicompyler import util
import SimpleITK as sitk
from pydicom import dcmread
from radiomics import featureextractor
import pandas as pd

def pluginProperties():
    """Properties of the plugin."""

    props = {}
    props['name'] = 'Pyradiomics Pipeline'
    props['menuname'] = "&Analyze...\tCtrl-Shift-P"
    props['description'] = "Start pyradiomics analysis"
    props['author'] = 'Sohaib Shahid'
    props['version'] = "0.1.0"
    props['plugin_type'] = 'import'
    props['plugin_version'] = 1
    props['min_dicom'] = []

    return props

class plugin:

    def __init__(self, parent):
        self.parent = parent

        # Initialize the import location via pubsub
        pub.subscribe(self.OnImportPrefsChange, 'general.dicom')
        pub.sendMessage('preferences.requested.values', msg = 'general.dicom')

        # Setup toolbar controls
        openbmp = wx.Bitmap(util.GetResourcePath('pipeline.png'))
        self.tools = [{'label':"pyRadiomics", 'bmp':openbmp,
                            'shortHelp':"Begin pyRadiomics analysis...",
                            'eventhandler':self.pluginMenu}]

    def OnImportPrefsChange(self, topic, msg):
        """When the import preferences change, update the values."""
        topic = topic.split('.')
        if (topic[1] == 'import_location'):
            self.path = str(msg)

    def pluginMenu(self, evt):
        """Generate pyradiomics spreadsheet."""

        patient_hash = ''
        if 'rtdose.dcm' in os.listdir(self.path):
            rtdose_file = dcmread(self.path + '/rtdose.dcm')
            patient_hash = os.path.basename(rtdose_file.PatientID)
        else:
            patient_hash = os.path.basename(self.path)
        converted_file_name = patient_hash + '.nrrd' # Name of nrrd file
        converted_file_location = self.path + '/nrrd/' # Location of folder where nrrd file saved
        converted_file_path = converted_file_location + converted_file_name # Complete path of converted file
        if not os.path.exists(converted_file_location): # If folder does not exist
            os.makedirs(converted_file_location) # Create folder
        
        # Convert dicom files to nrrd
        reader = sitk.ImageSeriesReader()
        dicomReader = reader.GetGDCMSeriesFileNames(self.path)
        reader.SetFileNames(dicomReader)
        dicoms = reader.Execute()
        sitk.WriteImage(dicoms, converted_file_path)
        
        print('DICOM to nrrd completed')

        # Convert rtstruct to nrrd
        # Each ROI is saved in separate nrrd files
        converted_struct_location = converted_file_location + 'structures' # Location of folder where converted masks saved
        cmd_for_segmask = 'plastimatch convert --input ' + self.path + '/rtss.dcm --output-prefix ' + converted_struct_location + ' --prefix-format nrrd --referenced-ct ' + self.path + ' 1>' + self.path + '/NUL' 
        cmd_del_nul = 'rm ' + self.path + '/NUL'
        os.system(cmd_for_segmask)
        os.system(cmd_del_nul)

        print('Segmentation masks converted')
       
        # Something went wrong, in this case PyRadiomics will also log an error
        if converted_file_path is None or converted_file_location is None: 
            print('Error getting testcase!')
            exit()
       
        # Initialize feature extractor using default pyradiomics settings
        # Default features: 
        #   first order, glcm, gldm, glrlm, glszm, ngtdm, shape
        # Default settings:
        #   'minimumROIDimensions': 2, 'minimumROISize': None, 'normalize': False, 
        #   'normalizeScale': 1, 'removeOutliers': None, 'resampledPixelSpacing': None, 
        #   'interpolator': 'sitkBSpline', 'preCrop': False, 'padDistance': 5, 'distances': [1], 
        #   'force2D': False, 'force2Ddimension': 0, 'resegmentRange': None, 'label': 1, 
        #   'additionalInfo': True 
        extractor = featureextractor.RadiomicsFeatureExtractor()

        print("Calculating features")
        
        all_features = [] # Contains the features for all the ROI
        radiomics_headers = [] # CSV headers
        feature_vector = ''

        for file in os.listdir(converted_struct_location):
            roi_features = [] # Contains features for current ROI
            roi_features.append(patient_hash)
            roi_features.append(self.path)
            mask_name = converted_struct_location + '/' + file # Full path of ROI nrrd file
            image_id = file.split('.')[0] # Name of ROI
            feature_vector = extractor.execute(converted_file_path, mask_name)
            roi_features.append(image_id)
            
            for feature_name in feature_vector.keys(): # Add first order features to list
                roi_features.append(feature_vector[feature_name])
            
            all_features.append(roi_features) 
        
        radiomics_headers.append('Hash ID')
        radiomics_headers.append('Directory Path')
        radiomics_headers.append('ROI') 

        # Extract column/feature names
        for feature_name in feature_vector.keys():
            radiomics_headers.append(feature_name)

        # Convert into dataframe
        radiomics_df = pd.DataFrame(all_features, columns = radiomics_headers)
        
        # Format dataframe to resemble that produced by Slicer3D
        radiomics_df.set_index('Hash ID', inplace=True)

        if not os.path.exists(self.path + '/CSV'): # If folder does not exist
            os.makedirs(self.path + '/CSV') # Create folder
        
        # Export dataframe as csv
        radiomics_df.to_csv(self.path + '/CSV/' + 'Pyradiomics_' + patient_hash + '.csv')

        print('\n' + 'Done')

        return
