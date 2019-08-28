import numpy as np
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