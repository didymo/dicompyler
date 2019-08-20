from src.Model.LoadPatients import *


# path = '/home/xudong/dicom_sample'
# dict_dataset = get_datasets_dict(path)
# print(dict_dataset)

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


def get_np_pixeldata(img_list, dict_ds):
    dict_pixel_data = {}
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
            dict_pixel_data[img] = ds._pixel_array
        else:
            print("Missing PixelData in " + img)
    return dict_pixel_data



if __name__ == "__main__":
    path = '/home/xudong/dicom_sample'
    dict_datasets = get_datasets_dict(path)
    namelist = get_namelist(dict_datasets)
    image_file_list = get_img_list(namelist, path)

    dict_raw_pixel_data = get_raw_pixeldata(image_file_list, dict_datasets)
    dict_np_pixel_data = get_np_pixeldata(image_file_list, dict_datasets)

    print(dict_raw_pixel_data.keys())
    print(type(dict_raw_pixel_data['/home/xudong/dicom_sample/ct.0.dcm']))

    print(dict_np_pixel_data.keys())
    print(type(dict_np_pixel_data['/home/xudong/dicom_sample/ct.0.dcm']))
    print(dict_np_pixel_data['/home/xudong/dicom_sample/ct.0.dcm'])

