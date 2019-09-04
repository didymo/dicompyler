import pydicom


def get_tree(ds, label=0):
    tree = []
    dont_print = ['Pixel Data', 'File Meta Information Version']
    # For all the elements in the dataset
    for elem in ds:
        curr_row = []
        # If it is a 'sequence'
        if elem.VR == "SQ":
            # Has Child?
            curr_row.append(label)
            curr_row.append(repr(elem.name))
            curr_row.append(repr(elem.tag))
            curr_row.append(repr(elem.VM))
            curr_row.append(repr(elem.VR))

            # Append to the return list
            tree.append(curr_row)
            # Recursive
            for seq_item in elem.value:
                items = get_tree(seq_item, 1)
            for item in items:
                tree.append(item)
        else:
            # Exclude pixel data and version info
            if elem.name not in dont_print:
                curr_row.append(label)
                curr_row.append(repr(elem.name))
                curr_row.append(repr(elem.value))
                curr_row.append(repr(elem.tag))
                curr_row.append(repr(elem.VM))
                curr_row.append(repr(elem.VR))
                # Append to the return list
                tree.append(curr_row)
    return tree


if __name__ == '__main__':
    path = '../../dicom_sample/ct.0.dcm'
    ds = pydicom.dcmread(path)
    ls = get_tree(ds, 0)
    for i in ls:
        print(i)

    print(ds)