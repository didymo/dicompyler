import pydicom
from pydicom.dataelem import DataElement_from_raw

ds = pydicom.dcmread("../../dicom_sample/ct.0.dcm")

# Iterating through the entire Dataset (including Sequences)
# content = []
# for item in ds.keys():
#     print(item)
#
# for item in ds.iterall():
#     DataElement_from_raw(item)
#   print(item.name + "\t" + str(item.VM) + "\t" + item.VR + "\t" + str(item.tag) + "\t" + str(item.value))
#

