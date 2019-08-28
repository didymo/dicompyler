"""
./src/Model/LoadPatients.py
This file contains basic functions for loading original dicom files.
The desired output should be a 'pydicom' defined type of dataset.
"""

import glob
import re
import logging
import pydicom
import os

# Create a logger for displaying info in the console.
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
load_logger = logging.getLogger()
# Change the logger level here, level WARN by default
load_logger.setLevel(logging.DEBUG)


# For sorting dicom file names by numbers
# Filename format example: "ct.0.dcm", "rtss.dcm", "rtdose.dcm"
# Input is a list of dcm file names.
# Return the sorted list of all file names.
path = '/home/xudong/dicom_sample'
def natural_sort(file_list):
    # Logger info
    load_logger.info('Natural Sorting...')
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(file_list, key=alphanum_key)


def get_datasets(path):
    dict_ds = {}
    dcm_files = natural_sort(glob.glob(path + '/*.dcm'))
    for i, file in enumerate(dcm_files):
        ds_tmp = pydicom.dcmread(file)
        if ds_tmp.SOPClassUID == '1.2.840.10008.5.1.4.1.1.2':
            img_file_name = os.path.basename(dcm_files[i])
            img_index = int(''.join(list(filter(str.isdigit, img_file_name))))
            dict_ds[img_index] = ds_tmp
        elif ds_tmp.SOPClassUID == '1.2.840.10008.5.1.4.1.1.481.3':
            dict_ds['rtss'] = ds_tmp
        elif ds_tmp.SOPClassUID == '1.2.840.10008.5.1.4.1.1.481.2':
            dict_ds['rtdose'] = ds_tmp
        elif ds_tmp.SOPClassUID == '1.2.840.10008.5.1.4.1.1.481.5':
            dict_ds['rtplan'] = ds_tmp
    return dict_ds