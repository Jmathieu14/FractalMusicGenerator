# Utility functions file
# Jacques Mathieu - 11/4/18

import os.path as osp
import os
import simplejson as j


# Create folder if it does not yet exist. Return the file path created
# See Source 1 for aid with this function (bottom of page)
def create_folder_if_dne(folder_name):
    full_path = osp.abspath(osp.curdir + "\\" + folder_name)
    if not osp.exists(full_path):
        os.makedirs(full_path)
    return full_path

# Write a list to a file in correct format to be read into MAX/MSP collections
# Also return the filepath used
def write_list_to_collection(filepath, list):
    ctr = 1
    with open(filepath, 'w') as my_file:
        for item in list:
            item = str(item)
            item = str.replace(item, "\\", "/")
            my_file.write(str(ctr) + " " + item + "\n")
            ctr = ctr + 1
    return filepath


# Write list to file with new line separated values
def write_list_to_file(filepath, list):
    ctr = 1
    with open(filepath, 'w') as my_file:
        for item in list:
            item = str(item)
            item = str.replace(item, "\\", "/")
            my_file.write(item + "\n")
            ctr = ctr + 1


# Convert hex string to base10 string
def hex_to_base10_string(hex):
    idxs_to_replace = []
    new_vals = []
    ctr = 0
    for c in hex:
        new_val = -1
        if (c == 'a'):
            new_val = 10
        elif (c == 'b'):
            new_val = 11
        elif (c == 'c'):
            new_val = 12
        elif (c == 'd'):
            new_val = 13
        elif (c == 'e'):
            new_val = 14
        elif (c == 'f'):
            new_val = 15

        if (new_val != -1):
            new_vals.append(new_val)
            idxs_to_replace.append(ctr)

        ctr = ctr + 1

    ctr = 0
    item_ct = idxs_to_replace.__len__()
    new_full_str = ""
    last_idx = 0

    for ctr in range(item_ct):
        new_str = str(new_vals[ctr])
        new_full_str += hex[last_idx:idxs_to_replace[ctr]] + new_str
        last_idx = idxs_to_replace[ctr] + 1

    # Add last part of string
    new_full_str += hex[last_idx:]

    return new_full_str


# Save json (or dict) to file
def json_to_file(my_json, filename):
    last_five_idx = filename.__len__() - 6
    last_five = filename[last_five_idx:]
    if (last_five.lower() != ".json"):
        filename = filename + ".json"
    filepath = osp.curdir + "\\json\\" + filename
    # If the full filepath was passed in...
    if filename.find(osp.curdir) >= 0:
        filepath = filename
    with open(filepath, 'w') as my_file:
        my_file.write(j.dumps(my_json, indent="\t"))
    return filename


# Print a dict object in a pretty manner
def pretty_print_json(my_json):
    print(j.dumps(my_json, indent="\t"))


# Return deep copy of given json
def copy_json(my_json):
    return j.loads(j.dumps(my_json))

# Scale an array of integers so they fit in the new bounds
def scale_integer_arr(n_arr, lowest_bound, top_bound):
    diff = top_bound - lowest_bound
    scaled_arr = []
    # print("top - bottom = " + str(diff))
    lowest_n = min(n_arr)
    top_n = max(n_arr)
    diff_n = top_n - lowest_n
    # print("n_arr max is %d and min is %d and diff is %d" % (top_n, lowest_n, diff_n))
    cap = n_arr.__len__()
    for idx in range(cap):
        scaled_arr.append(int((diff * ((n_arr[idx] - lowest_n)/diff_n)) + lowest_bound))
    # print("transformed list:")
    # print(scaled_arr)
    return scaled_arr


# Source 1:
# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
# Blair Conrad's answer