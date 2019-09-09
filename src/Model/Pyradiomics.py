"""
This file contains the functionality required for the pyradiomics analysis
"""

import os
import pandas as pd
import SimpleITK as sitk
from pydicom import dcmread
from radiomics import featureextractor


def pyradiomics(path):
    """Generate pyradiomics spreadsheet."""

    patient_hash = ''
    if 'rtdose.dcm' in os.listdir(path):
        rtdose_file = dcmread(path + '/rtdose.dcm')
        patient_hash = os.path.basename(rtdose_file.PatientID)
    else:
        patient_hash = os.path.basename(path)

    converted_file_name = patient_hash + '.nrrd'  # Name of nrrd file
    converted_file_location = path + '/nrrd/'  # Location of folder where nrrd file saved
    converted_file_path = converted_file_location + converted_file_name  # Complete path of converted file

    if not os.path.exists(converted_file_location):  # If folder does not exist
        os.makedirs(converted_file_location)  # Create folder

    # Convert dicom files to nrrd
    reader = sitk.ImageSeriesReader()
    dicomReader = reader.GetGDCMSeriesFileNames(path)
    reader.SetFileNames(dicomReader)
    dicoms = reader.Execute()
    sitk.WriteImage(dicoms, converted_file_path)

    print('DICOM to nrrd completed')

    # Convert rtstruct to nrrd
    # Each ROI is saved in separate nrrd files
    converted_struct_location = converted_file_location + 'structures'  # Location of folder where converted masks saved
    cmd_for_segmask = 'plastimatch convert --input ' + path + '/rtss.dcm --output-prefix ' + converted_struct_location + ' --prefix-format nrrd --referenced-ct ' + path + ' 1>' + path + '/NUL'
    cmd_del_nul = 'rm ' + path + '/NUL'
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

    all_features = []  # Contains the features for all the ROI
    radiomics_headers = []  # CSV headers
    feature_vector = ''

    for file in os.listdir(converted_struct_location):
        roi_features = []  # Contains features for current ROI
        roi_features.append(patient_hash)
        roi_features.append(path)
        mask_name = converted_struct_location + '/' + file  # Full path of ROI nrrd file
        image_id = file.split('.')[0]  # Name of ROI
        feature_vector = extractor.execute(converted_file_path, mask_name)
        roi_features.append(image_id)

        for feature_name in feature_vector.keys():  # Add first order features to list
            roi_features.append(feature_vector[feature_name])

        all_features.append(roi_features)

    radiomics_headers.append('Hash ID')
    radiomics_headers.append('Directory Path')
    radiomics_headers.append('ROI')

    # Extract column/feature names
    for feature_name in feature_vector.keys():
        radiomics_headers.append(feature_name)

    # Convert into dataframe
    radiomics_df = pd.DataFrame(all_features, columns=radiomics_headers)

    radiomics_df.set_index('Hash ID', inplace=True)

    if not os.path.exists(path + '/CSV'):  # If folder does not exist
        os.makedirs(path + '/CSV')  # Create folder

    # Export dataframe as csv
    radiomics_df.to_csv(path + '/CSV/' + 'Pyradiomics_' + patient_hash + '.csv')

    print('\n' + 'Pyradiomics csv generated.')

    return


if __name__ == '__main__':
    path = '/home/sohaib/992/DICOM/OK.please.anonymise'
    pyradiomics(path)
