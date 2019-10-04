# Abstracted Collection Generator
# Jacques Mathieu - 12/2/18

MAX_PITCH = 20000
MIN_PITCH = 20


def hgen_asc_float_coll(params):
    base_dur = params['base_num']
    max_dur = params['max_num']
    float_coll = []
    iter = params['iter']
    cur_num = base_dur
    while (cur_num < max_dur):
        float_coll.append(cur_num)
        cur_num = cur_num + iter

    return float_coll


def hgen_desc_float_coll(params):
    base_dur = params['base_num']
    max_dur = params['max_num']
    float_coll = []
    iter = params['iter']
    cur_num = max_dur
    while (cur_num > base_dur):
        float_coll.append(cur_num)
        cur_num = cur_num - iter

    return float_coll


def hgen_repeat_float_coll(params):
    my_list = []
    my_list.append(params['base_num'])
    return my_list


def hgen_mult_asc_float_coll(params):
    min = params['base_num']
    max = params['max_num']
    float_coll = []
    scalar = params['scalar']
    if scalar < 1.0:
        scalar = scalar + 1.0
    cur_num = min
    while (cur_num < max):
        float_coll.append(cur_num)
        cur_num = cur_num * scalar
    return float_coll


def hgen_mult_desc_float_coll(params):
    float_coll = hgen_mult_asc_float_coll(params)
    float_coll_rev = []
    fc_len = float_coll.__len__()
    for x in range(1, fc_len + 1):
        float_coll_rev.append(float_coll[fc_len - x])

    return float_coll_rev


def gen_float_coll(method, params):
    print("Method is: " + method)
    if method == "asc":
        return hgen_asc_float_coll(params)
    elif method == "desc":
        return hgen_desc_float_coll(params)
    elif method == "repeat":
        return hgen_repeat_float_coll(params)
    elif method == "mult_asc":
        return hgen_mult_asc_float_coll(params)
    elif method == "mult_desc":
        return hgen_mult_desc_float_coll(params)


# -------------------------------------------------------------------------------------------- #
#                                     PITCH GENERATION
# -------------------------------------------------------------------------------------------- #

# Generate a pitch collection given the lowest pitch and other specs (such as generation mode)
def gen_pitch_collection(base_pitch, mode_specs):
    if mode_specs['mode'] == "ET":
        return hgen_ET_pitch_collection(base_pitch, mode_specs)

# Generate a list that represents a pitch collection in which
# the lowest pitch is the base_pitch, each octave is generated
# from multiplying the base pitch with the base multiple and
# each octave is divided into ET_div equal parts
def hgen_ET_pitch_collection(base_pitch, mode_specs):
    base_multiple = mode_specs['base_multiple']
    ET_div = mode_specs['ET_div']
    scale_mode_specified = 0
    if "scale_mode" in mode_specs:
        scale_mode_specified = 1
    pitch_coll = []
    octaves = [] # List to store the octave frequencies

    base_pitch = float(base_pitch)
    base_multiple = float(base_multiple)
    # ET_div = float(ET_div)
    if (base_pitch < MIN_PITCH):
        base_pitch = MIN_PITCH

    cur_pitch = base_pitch
    cur_oct = 0
    cur_octave_pitch = base_pitch

    # store our octave pitches in the octave list
    while (cur_octave_pitch < MAX_PITCH):
        octaves.append(cur_octave_pitch)
        cur_octave_pitch = cur_octave_pitch * base_multiple

    last_oct = octaves.__len__() - 1

    while (cur_oct < last_oct):
        cur_oct_freq = octaves[cur_oct]
        # print("Current octave: " + str(cur_oct_freq))
        freq_diff = octaves[cur_oct + 1] - cur_oct_freq
        # print("freq diff: " + str(freq_diff))
        for x in range(ET_div):
            numerator = float(x)
            add_note = 1
            if scale_mode_specified:
                if not x in mode_specs['scale_mode']:
                    add_note = 0

            if add_note:
                new_pitch = cur_oct_freq * base_multiple**(numerator/ET_div)
                pitch_coll.append(new_pitch)

        cur_oct = cur_oct + 1

    # Put the last octave on the end of the pitch collection
    pitch_coll.append(octaves[last_oct])
    return pitch_coll