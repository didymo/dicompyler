import pydicom
import numpy as np
from src.Model.LoadPatients import *
import matplotlib.pyplot as plt

# Delete ROI by name
def delete_roi(rtss, roi_name):
    # ROINumber
    roi_number = -1
    # Delete related StructureSetROISequence element
    for i, elem in enumerate(rtss.StructureSetROISequence):
        if elem.ROIName == roi_name:
            roi_number = rtss.StructureSetROISequence[i].ROINumber
            del rtss.StructureSetROISequence[i]

    # Delete related ROIContourSequence element
    for i, elem in enumerate(rtss.ROIContourSequence):
        if elem.ReferencedROINumber == roi_number:
            del rtss.ROIContourSequence[i]

    # Delete related RTROIObservationsSequence element
    for i, elem in enumerate(rtss.RTROIObservationsSequence):
        if elem.ReferencedROINumber == roi_number:
            del rtss.RTROIObservationsSequence[i]

    return rtss


# Return a dictionary of all the contour points of the ROI, slice by slice (if exists)
# Key: ReferencedSOPInstanceUID, Value: ContourData
# ContourData: It looks like a list of values, but it is composed by many 3-item coordinate sets.
# (x, y, z)
# More Info: https://dicom.innolitics.com/ciods/rt-structure-set/roi-contour/30060039/30060040/30060050
def get_raw_contours(rtss, roi_name):
    # The index of the ROI
    roi_number = -1
    # Create a return dictionary
    dict_contours = {}
    # Get the ROI index, and store it for finding the related ROI contour data
    for i, elem in enumerate(rtss.StructureSetROISequence):
        if roi_name == rtss.StructureSetROISequence[i].ROIName:
            roi_number = rtss.StructureSetROISequence[i].ROINumber
            break
    # Loop among every ROI in the ROI contour sequence
    for roi in rtss.ROIContourSequence:
        # Find the target ROI
        if roi.ReferencedROINumber == roi_number:
            # For each slice which contains the ROI
            for slice in roi.ContourSequence:
                # Get the identifier of current slice (with the ROI)
                # Store it, and use it as the key of the dictionary
                for img_seq in slice.ContourImageSequence:
                    # print(img_seq.ReferencedSOPInstanceUID)
                    SOP_UID = img_seq.ReferencedSOPInstanceUID
                contour_data = slice.ContourData
                dict_contours[SOP_UID] = contour_data
                # print(slice)
                # print(slice.ContourData)
                # print(slice.NumberOfContourPoints)
                # print(slice.ContourImageSequence)
            # for slice in roi:
            #     print(slice)
            #     # dict_contours[slice.ReferencedSOPInstanceUID] = slice.ContourData
            # break
    return dict_contours


# Get the transformation matrix from a IMAGE dataset
def get_transform_matrix(img_ds):
    # Physical distance (in mm) between the center of each image pixel, specified by a numeric pair
    # - adjacent row spacing (delimiter) adjacent column spacing.
    dist_row = img_ds.PixelSpacing[0]
    dist_col = img_ds.PixelSpacing[1]
    # The direction cosines of the first row and the first column with respect to the patient.
    # 6 values inside: [Xx, Xy, Xz, Yx, Yy, Yz]
    orientation = img_ds.ImageOrientationPatient
    # The x, y, and z coordinates of the upper left hand corner
    # (center of the first voxel transmitted) of the image, in mm.
    # 3 values: [Sx, Sy, Sz]
    position = img_ds.ImagePositionPatient

    # Equation C.7.6.2.1-1.
    # https://dicom.innolitics.com/ciods/rt-structure-set/roi-contour/30060039/30060040/30060050
    matrix_M = np.matrix(
        [[orientation[0]*dist_row, orientation[3]*dist_col, 0, position[0]],
         [orientation[1]*dist_row, orientation[4]*dist_col, 0, position[1]],
         [orientation[2]*dist_row, orientation[5]*dist_col, 0, position[2]],
         [0, 0, 0, 1]]
    )
    x = []
    y = []
    for i in range(0, img_ds.Columns):
        i_mat = matrix_M * np.matrix([[i], [0], [0], [1]])
        x.append(float(i_mat[0]))

    for j in range(0, img_ds.Rows):
        j_mat = matrix_M * np.matrix([[0], [j], [0], [1]])
        y.append(float(j_mat[1]))

    return (np.array(x), np.array(y))

def get_contour_pixel_data(pixlut, contour, prone = False, feetfirst = False):
    contour_pixel_data = []

    for i in range(0, len(contour), 3):
        for x, x_val in enumerate(pixlut[0]):
            if(x_val > contour[i] and not prone and not feetfirst):
                break
            elif (x_val < contour[i]):
                if feetfirst or prone:
                    break
        for y, y_val in enumerate(pixlut[1]):
            if (y_val > contour[i+1] and not prone):
                break
            elif (y_val < contour[i+1] and prone):
                break
        contour_pixel_data.append((x, y))
    return contour_pixel_data


# pixeldata = self.GetContourPixelData(self.structurepixlut, contour['data'], prone, feetfirst)
# def get_contour(lut, contour, prone=False, feetfirst=False):
#     pixeldata = []
    # for i, point in enumerate(contour):
    #     for x, x_val in enumerate(pix):


def main():
    path = '../../../dicom_sample'
    dict_ds, path = get_datasets(path)
    rtss = dict_ds['rtss']

    ### GTVp is the 10th ROI in the sequence
    # (3006, 0022) ROI Number                          IS: "10"
    # (3006, 0024) Referenced Frame of Reference UID   UI: 1.3.12.2.1107.5.1.4.100020.30000018082923183405900000003
    # (3006, 0026) ROI Name                            LO: 'GTVp'
    # (3006, 0036) ROI Generation Algorithm            CS: 'SEMIAUTOMATIC'

    # (3006, 002a) ROI Display Color IS: ['255', '0', '0']
    # (3006, 0040) Contour Sequence 15 item(s) - ---

    roi_name = 'EYE_L'

    dict_contours = get_raw_contours(rtss, roi_name)

    roi_slice_list = []

    # Get all the slice UID which contains the ROI
    for key in dict_contours:
        roi_slice_list.append(key)
        # print(key)

    dict_transform_matrices = {}

    for key in dict_ds:
        ds = dict_ds[key]
        if ds.SOPClassUID == '1.2.840.10008.5.1.4.1.1.2':
            if ds.SOPInstanceUID in roi_slice_list:
                pixlut = get_transform_matrix(ds)
                dict_transform_matrices[ds.SOPInstanceUID] = pixlut

    for key in dict_transform_matrices:
        print(key)



    pixel_contours = []
    for key in dict_transform_matrices:
        contour = dict_contours[key]
        pixlut = dict_transform_matrices[key]
        contour_pixel_data = get_contour_pixel_data(pixlut, contour)
        # print(contour_pixel_data)
        pixel_contours.append(contour_pixel_data)
    print(len(pixel_contours))
    xs = []
    ys = []
    for point in pixel_contours[8]:
        xs.append(point[0])
        ys.append(-1 * point[1])
    plt.scatter(xs, ys)
    plt.xlim(270, 300)
    plt.ylim(-210, -180)
    plt.show()


if __name__ == '__main__':
    main()