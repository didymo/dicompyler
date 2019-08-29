import numpy as np
from dicompylercore import dvhcalc
import pydicom
import matplotlib.pyplot as plt


def dvh_plot(dvh):
    plt.plot(dvh.bincenters, dvh.counts, label=dvh.name,
             color=None if not isinstance(dvh.color, np.ndarray) else
             (dvh.color / 255))
    plt.xlabel('Dose [%s]' % dvh.dose_units)
    plt.ylabel('Volume [%s]' % dvh.volume_units)
    if dvh.name:
        plt.legend(loc='best')
    return dvh


# if __name__ == '__main__':
#     path = '/home/xudong/dicom_sample/'
#     rtss_path = path + 'rtss.dcm'
#     rtdose_path = path + 'rtdose.dcm'
#
#     ds_rtdose = pydicom.dcmread(rtdose_path)
#     ds_rtss = pydicom.dcmread(rtss_path)
#
#     dvh = dvhcalc.get_dvh(ds_rtss, ds_rtdose, 13)
#     dvh_plot(dvh)
#     plt.show()
