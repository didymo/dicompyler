import numpy as np
from src.Model.LoadPatients import *


def get_img():



# This is for getting the raw data from dcm file
# The data is in 'bytes' type
def get_raw_pixeldata(img_list, dict_ds):
    dict_pixel_data = {}
    for img in img_list:
        # print(img)
        ds = dict_ds[img]
        if "PixelData" in ds:
            dict_pixel_data[img] = ds.PixelData
        else:
            print("Missing PixelData in " + img)
    return dict_pixel_data


# Get a dictionary of numpy.ndarray pixel data.
# Key: full path of the original file
# Value: numpy.ndarray (after preprocessing)
def get_np_pixeldata(img_list, dict_ds):
    dict_pixel_data = {}    # Create a empty dictionary for pixel data
    #
    for img in img_list:
        # print(img)
        ds = dict_ds[img]
        if "PixelData" in ds:
            # Convert pixel data (raw type) into numpy.ndarray
            # https://pydicom.github.io/pydicom/stable/_modules/pydicom/dataset.html#Dataset.convert_pixel_data
            ds.convert_pixel_data()
            # Store the numpy.ndarray in the dictionary
            # The numpy.ndarray is stored internally in the dataset
            # with keyword _pixel_array
            np_pixel = ds._pixel_array

            # Preprocessig data
            max_val = np.amax(np_pixel) # Get the maximum value of pixel data
            min_val = np.amin(np_pixel) # Get the minimum value of pixel data
            # Preprocessing
            np_pixel = (np_pixel - min_val) / (max_val - min_val) * 256
            # Set upper and lower bound of values
            np_pixel[np_pixel < 0] = 0
            np_pixel[np_pixel > 255] = 255
            # Change the type of values to int8
            np_pixel = np_pixel.astype("int8")
            # Save the pixel data to the dictionary
            dict_pixel_data[img] = np_pixel
        else:
            print("Missing PixelData in " + img)

    return dict_pixel_data

