import pydicom


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



def main():
    path = '../../../dicom_sample/'
    rtss = pydicom.dcmread(path + 'rtss.dcm')

    # roi_name = 'GTVp'
    # rtss = delete_from_rtss(rtss, roi_name)



if __name__ == '__main__':
    main()
