# This be the place for yer fractal functions!
# Jacques Mathieu - 10/31/18
import simplejson as j
import codecs
import re
import utility as util
import random

def read_input_to_var(f):
    with open(f, 'r') as my_file:
        s = my_file.read()
    my_in = j.loads(s)
    return my_in


# Get the correct sequence given the starting item
def get_sequence_from_fractal_rules(item, rules):
    for arr in rules:
        if item == arr[0]:
            # print("Rules found for item: " + str(item))
            return arr
    # In case where there are no rules for the specified item
    # print("Rules not found for item: " + str(item))
    return None


# Generate a fractal sequence of depth d
def gen_d_level_fractal(my_json, depth):
    fr_seq = my_json['raw_fractal_data'][0]
    res = []
    prev_seq = util.copy_json(fr_seq)
    res.extend(prev_seq)
    add_eos = ('EOS' in my_json)
    # Add first EOS if specified
    if add_eos:
        res.append(my_json['EOS'])

    for x in range(1, depth):
        level_x_seq = gen_d_level_fractal_helper(prev_seq, my_json, x-1, x)
        res.extend(level_x_seq)
        if add_eos:
            res.append(my_json['EOS'])
        prev_seq = level_x_seq

    # res = gen_d_level_fractal_helper(fr_seq, my_json, 0, depth)

    # Map data to generated raw fractal sequence
    idx_arr = my_json['raw_idx_list']
    mapped_data = my_json['mapped_data']
    ctr = 0
    for n in res:
        if n in idx_arr:
            res[ctr] = mapped_data[idx_arr.index(n)]
        ctr = ctr + 1

    return res


# Helper function for generating a fractal sequence of depth d
def gen_d_level_fractal_helper(prev_seq, my_json, ctr, max_depth):
    fractal_rules = my_json['raw_fractal_data']
    cur_seq = []

    if ctr < max_depth:
        for item in prev_seq:
            arr = get_sequence_from_fractal_rules(item, fractal_rules)
            if (arr != None):
                # print("Extending sequence")
                cur_seq.extend(arr)
            else:
                cur_seq.append(item)

        ctr = ctr + 1
        return gen_d_level_fractal_helper(cur_seq, my_json, ctr, max_depth)
    else:
        return prev_seq


# Write a fractal to file and return the file name
def fractal_to_file(my_fractal, my_dir):
    hex_len = my_fractal['hex'].__len__()
    voice_id = ""
    scalar_str = ""
    if 'voice_id' in my_fractal:
        voice_id = my_fractal['voice_id']
    if 'scalar' in my_fractal:
        scalar_str = "min" + str(int(my_fractal['scalar']['min'] * 100)) + "_" + \
               "max" + str(int(my_fractal['scalar']['max'] * 100)) + "_"
    filename = my_fractal['hex'][:7]
    filename = filename + my_fractal['hex'][hex_len - 6:]
    filename = my_dir + "\\" + voice_id + "p" + str(my_fractal['pattern_length']) + "_" +  "type_" + scalar_str + \
               my_fractal['data_type'] + filename
    util.json_to_file(my_fractal, filename)
    return filename


# Convert hex string to array of decimal numbers in a lossy manner
def hex_seed_to_number_arr_lossy(seed):
    seed = re.sub('[a-z]|[A-Z]', '', seed)
    number_arr = []
    seed_len = seed.__len__()
    # If we do not have an even number of chars, fix that!
    if (seed_len % 2 != 0):
        seed.__add__("0")
        seed_len = seed_len + 1
        print("Added 0 to end of hex [Lossy version being used]")
    seed_len = int((seed_len/2) - 0.5)
    for x in range(seed_len):
        idx = x * 2
        slice = seed[idx] + seed[idx + 1]
        number_arr.append(int(slice))
    return number_arr


# Convert hex string to array of decimal numbers
def hex_seed_to_number_arr(seed):
    number_arr = []
    seed_len = seed.__len__()
    # If we do not have an even number of chars, fix that!
    if (seed_len % 2 != 0):
        seed.__add__("0")
        seed_len = seed_len + 1
        print("Added 0 to end of hex seed")
    seed_len = int((seed_len/2) - 0.5)
    # https://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python
    # Help on hex to decimal conversion from post above, answer by Dan Lenski
    for x in range(seed_len):
        idx = x * 2
        slice = seed[idx] + seed[idx + 1]
        number_arr.append(int(slice, 16))
    return number_arr


# A basic method to generate a fractal pattern given the data_location (which is essentially the field on
# the fractal where it appears) of the data to be 'fractalized'.
# This pattern will be saved on 'my_fractal' given the 'fractal_pattern_location'
def gen_basic_fractal_pattern(my_fractal, data_location, fractal_pattern_location):
    # Make sure save the location has the correct formatting
    my_fractal[fractal_pattern_location] = [[]]
    data = my_fractal[data_location]
    pattern_length = my_fractal['pattern_length']
    cap = data.__len__()
    data_row_idx = 0
    for i in range(cap):
        if (i != 0 and i % pattern_length == 0):
            data_row_idx = data_row_idx + 1
            my_fractal[fractal_pattern_location].append([])
        my_fractal[fractal_pattern_location][data_row_idx].append(data[i])

# Make a fractal json from a list of indices and set pattern length
# To be deprecated
# def make_fractal_json(my_list, pattern_length, min_percent, max_percent, hex_str, seed_str):
#     my_fractal = {"hex":hex_str, "seed":seed_str, "pattern_length":pattern_length,
#                   "min_percent":min_percent, "max_percent":max_percent,
#                   "idx_list":my_list,
#                   "fractal_data":[[]]} # Set up the skeleton of our fractal to be
#
#     cap = my_list.__len__()
#     data_row_idx = 0
#     for i in range(cap):
#         if (i != 0 and i % pattern_length == 0):
#             data_row_idx = data_row_idx + 1
#             my_fractal['fractal_data'].append([])
#         my_fractal['fractal_data'][data_row_idx].append(my_list[i])
#
#     print(my_fractal)
#     return my_fractal

# Make a raw fractal json
def make_raw_fractal_json(raw_idx_list, pattern_length, seed_str, params):
    my_fractal = {"data_type":"raw", "seed":seed_str, "pattern_length":pattern_length,
                  "raw_idx_list":raw_idx_list,
                  "raw_fractal_data":[[]]} # Set up the skeleton of our fractal to be
    if params != None and "array" in params:
        cap = params['array'].__len__()
        for x in range(cap):
            param_name = params['array'][x]
            if param_name in params:
                my_fractal[param_name] = params[param_name]
            else:
                print("%s not in params object" % (param_name))

    gen_basic_fractal_pattern(my_fractal, "raw_idx_list", "raw_fractal_data")

    # cap = raw_idx_list.__len__()
    # data_row_idx = 0
    # for i in range(cap):
    #     if (i != 0 and i % pattern_length == 0):
    #         data_row_idx = data_row_idx + 1
    #         my_fractal['raw_fractal_data'].append([])
    #     my_fractal['raw_fractal_data'][data_row_idx].append(raw_idx_list[i])

    return my_fractal


# Change the given number array to use the values of the pitch collection passed in
def map_idx_list_to_data(idx_list, data):
    mapped_data = []
    cap = idx_list.__len__()
    for i in range(cap):
        mapped_data.append(data[idx_list[i]])

    return mapped_data

ret_dict_number_arr_key = "number_arr"

def seed_to_raw_fractal(seed, pattern_length, seed_parse_mode):
    if (seed != None):
        seed_number_arr = []
        original_seed = seed
        # Return object for parsing modes
        ret_dict = {}
        if (seed_parse_mode == "hex_to_dec_lossy"):
            ret_dict = parse_seed_hex_to_dec_lossy(seed)
            seed_number_arr = ret_dict[ret_dict_number_arr_key]
        elif (seed_parse_mode == "hex_to_dec"):
            ret_dict = parse_seed_hex_to_dec(seed)
            seed_number_arr = ret_dict[ret_dict_number_arr_key]
        # If number array full
        if (seed_number_arr.__len__() >= pattern_length):
            # seed_pitch_arr = map_idx_list_to(seed_number_arr, pitch_col)
            return make_raw_fractal_json(seed_number_arr, pattern_length, original_seed, ret_dict)
        else:
            # Error!
            print("Pattern length of %d is too long for given seed.\n Try a longer seed or shorter pattern length." %
                  (pattern_length))


def str_to_hex(str):
    return str.encode().hex()

def parse_seed_hex_to_dec(seed):
    key1 = "hex"
    ret_dict = {}
    ret_dict['array'] = []
    ret_dict['array'].append(key1)
    seed = str_to_hex(seed)
    ret_dict[key1] = seed
    seed = util.hex_to_base10_string(seed)
    # The number array that will become the raw version of the fractal pattern
    ret_dict[ret_dict_number_arr_key] = hex_seed_to_number_arr(seed)
    return ret_dict


def parse_seed_hex_to_dec_lossy(seed):
    key1 = "hex"
    ret_dict = {}
    ret_dict['array'] = []
    ret_dict['array'].append(key1)
    seed = str_to_hex(seed)
    ret_dict[key1] = seed
    seed = util.hex_to_base10_string(seed)
    # The number array that will become the raw version of the fractal pattern
    ret_dict[ret_dict_number_arr_key] = hex_seed_to_number_arr_lossy(seed)
    return ret_dict



# Apply our fractal and modify it to map the raw data to the replacement data (i.e. frequencies, time, etc.)
# Any defined scalar are also applied first to make sure the data is compatible.
# Will also label fractal with the data type (of the replacement data)
def apply_fractal_to_data(raw_fractal, scalar, rep_data, data_type):
    raw_frac_copy = util.copy_json(raw_fractal)
    mapped_data_arr = []

    # Get the lowest and highest indexes to which our raw data will be mapped to.
    # These indexes are from the replacement data, modified via the specified scalar values.
    max_rep_data_idx = rep_data.__len__() - 1
    min_rep_data_idx = int(scalar['min'] * max_rep_data_idx)
    max_rep_data_idx = int(scalar['max'] * max_rep_data_idx)

    print("Ranges for " + data_type + " are from %d to %d" % (min_rep_data_idx, max_rep_data_idx))

    scaled_raw_data_arr = util.scale_integer_arr \
        (raw_frac_copy['raw_idx_list'], min_rep_data_idx, max_rep_data_idx)
    raw_frac_copy['scaled_idx_list'] = scaled_raw_data_arr
    raw_frac_copy['data_type'] = data_type
    mapped_data_arr = map_idx_list_to_data(scaled_raw_data_arr, rep_data)
    raw_frac_copy['mapped_data'] = mapped_data_arr
    raw_frac_copy['scalar'] = scalar
    pattern_length = raw_frac_copy['pattern_length']
    gen_basic_fractal_pattern(raw_frac_copy, "mapped_data", "fractal_data")

    unique_raw_indices = len(set(raw_frac_copy['raw_idx_list']))
    unique_mapped_data_points = len(set(raw_frac_copy['mapped_data']))
    percent_lossage_avoided = (float(unique_mapped_data_points - unique_raw_indices)/float(unique_raw_indices)) * 100.0

    if percent_lossage_avoided != 0.0:
        print("\nSmart mapping prevented using a sequence of %d data points and instead used %d" %
              (unique_mapped_data_points, unique_raw_indices))

        print("This avoided a " + str(percent_lossage_avoided) + "% delta of change in the resulting fractal sequence\n")

    return raw_frac_copy


# Generate a random seed for making a fractal using the given string
def gen_fractal_seed(my_str):
    p_len = my_str.__len__()
    char_list = []
    ret_str = my_str
    for x in range(1, p_len + 1):
        char_list.append(my_str[x-1:x])
    # int.__rand__()
    print(char_list)
    for i in range(1, p_len):
        cur_char = char_list[i]
        rand_word = cur_char
        for y in range(1, p_len):
            rand_word = rand_word + char_list[random.randint(0, p_len - 1)]
        # print("New word is: " + rand_word)
        ret_str = ret_str + rand_word

    print("Random seed is: " + ret_str)
    return ret_str



# def seed_to_pitch_fractal(seed, pitch_col, min_percent, max_percent, pattern_length):
#     raw_fractal = seed_to_raw_fractal(seed, pattern_length)
#     seed_number_arr = raw_fractal['raw_idx_list']
