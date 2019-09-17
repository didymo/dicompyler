import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.LoadPatients import *


def get_img(dict_ds):
    dict_img = {}
    non_img_list = ['rtss', 'rtdose', 'rtplan']
    for key in dict_ds:
        if key not in non_img_list:
            ds = dict_ds[key]
            ds.convert_pixel_data()

            np_pixels = ds._pixel_array
            max_val = np.amax(np_pixels)
            min_val = np.amin(np_pixels)
            np_pixels = (np_pixels - min_val) / (max_val - min_val) * 256
            np_pixels[np_pixels < 0] = 0
            np_pixels[np_pixels > 255] = 255
            np_pixels = np_pixels.astype("int8")

            dict_img[key] = np_pixels
    return dict_img


# Return a dictionary of pixmaps for UI
def get_pixmaps(dict_ds):
    # Create a dictionary of storing pixmaps
    dict_pixmaps = {}
    # List of non-image keys
    non_img_list = ['rtss', 'rtdose', 'rtplan']
    # Loop all the keys in dictionary of datasets
    for key in dict_ds:
        # Focus on the image files
        if key not in non_img_list:
            # Get current dataset
            ds = dict_ds[key]
            # convert the raw pixel data in to numpy array
            ds.convert_pixel_data()
            # Get the numpy array pixel data
            np_pixels = ds._pixel_array
            # Preprocessing it for better looking
            max_val = np.amax(np_pixels)
            min_val = np.amin(np_pixels)
            np_pixels = (np_pixels - min_val) / (max_val - min_val) * 255
            np_pixels[np_pixels < 0] = 0
            np_pixels[np_pixels > 255] = 255
            np_pixels = np_pixels.astype("int8")
            # Convert numpy array data to qimage for pyqt5
            qimage = QtGui.QImage(np_pixels, np_pixels.shape[1], np_pixels.shape[0], QtGui.QImage.Format_Indexed8)
            pixmap = QtGui.QPixmap(qimage)
            pixmap = pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio)

            dict_pixmaps[key] = pixmap
    return dict_pixmaps


# if __name__ == "__main__":
#     path = '/home/xudong/dicom_sample'
#     ds = get_datasets(path)
#     img_dict = get_img(ds)
#     for key in img_dict:
#         print(type(key))
