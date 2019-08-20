"""
./src/Model/LoadPatients.py
This file contains basic functions for loading original dicom files.
The desired output should be a 'pydicom' defined type of dataset.
"""

import glob
import re
import logging
import pydicom


# Create a logger for displaying info in the console.
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
load_logger = logging.getLogger()
# Change the logger level here, level WARN by default
load_logger.setLevel(logging.DEBUG)


# For sorting dicom file names by numbers
# Filename format example: "ct.0.dcm", "rtss.dcm", "rtdose.dcm"
# Input is a list of dcm file names.
# Return the sorted list of all file names.
def natural_sort(file_list):
    # Logger info
    load_logger.info('Natural Sorting...')
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(file_list, key=alphanum_key)


# Get all the file names in the given directory which contains dcm image files.
# (rtss, rtdose excluded)
# Input is the given directory
# Return the sorted name list
def get_dcm_names(path):
    # Retrieve all the file names in a list
    dcm_file_names = glob.glob(path+"/ct.?*.dcm")
    # Natural sort the list
    dcm_file_names = natural_sort(dcm_file_names)
    # Logger debug, showing the list after sorting.
    load_logger.debug('Got the dcm file names: %s', dcm_file_names)
    return dcm_file_names


# Return the a list of dataset of image dcm files.
# Reminder the return value is a list of datasets
# First dataset from: ct.0.dcm
def get_datasets(path):
    # Create a new list for datasets
    datasets = []
    # Get all the names
    dcm_files = get_dcm_names(path)
    # Convert dcm into datasets, and append to the list.
    for file in dcm_files:
        ds = pydicom.dcmread(file)
        # Xudong: idk if this one is necessary.
        # If all the files "ct.*.dcm" contains PixelData,
        # Then discard the if statement.
        if 'PixelData' in ds:
            datasets.append(ds)
    return datasets


def get_datasets_dict(path):
    dict_datasets = {}
    dcm_file_names = glob.glob(path + "/*.dcm")
    for file in dcm_file_names:
        ds = pydicom.dcmread(file)
        dict_datasets[file] = ds
    return dict_datasets


def get_namelist(dict_ds):
    name_list = list(dict_ds.keys())
    name_list = natural_sort(name_list)
    return name_list


def get_img_list(namelist, path):
    img_list = []
    index = 0
    name = path + "/ct." + str(index) + ".dcm"
    while name in namelist:
        img_list.append(name)
        index = index + 1
        name = path + "/ct." + str(index) + ".dcm"
    return img_list



"""
Codes below is for testing only.
"""
if __name__ == '__main__':
    path = '/home/xudong/dicom_sample'
    # datasets = get_datasets(path)
    dict_datasets = get_datasets_dict(path)
    namelist = get_namelist(dict_datasets)
    img_list = get_img_list(namelist, path)
    print(img_list)

"""
End of Testing
"""