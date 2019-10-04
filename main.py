# This be the main file!
# Jacques Mathieu - 10/31/18
import fractal_functions as ff
import utility as util
import coll_generator as cg
import os.path as osp

WRITE_FALSE = False
WRITE_TRUE = True
MAX_SCALAR = {'min': 0.0, 'max': 1.0}


# Parse the indicated pitch section, given the correct index from a section of a config file
def process_pitch_config(voices, y, seeds, paths, piece, max_config):
    p_instructions = voices[y]['pitch_inst']
    p_coll = p_instructions['pitch_coll']
    voice_p_seed = p_instructions['seed']
    voice_master_scalar = voices[y]['master_scalar']
    voice_id = "v" + str(y + 1)

    # VOICE PITCH ----------------------------------------------------------------------------

    # If the seed for the pitches of a voice is set to a number, treat it as a number
    # indicating the seed to use that has been previously mentioned in the file (way to reuse
    # seed without typing it twice)
    if type(voice_p_seed) == int and seeds != None and voice_p_seed <= seeds.__len__():
        voice_p_seed = seeds[voice_p_seed - 1]
    elif type(voice_p_seed) == int and seeds != None and voice_p_seed > seeds.__len__():
        print("Error, seed of index " + str(voice_p_seed) + " is out of bounds. Please fix this error.")
    else:
        seeds.append(voice_p_seed)

    # Set up the scalar we will be using for the pitches
    voice_p_scalar = {}
    if 'use_master_scalar' in p_instructions and p_instructions['use_master_scalar']:
        voice_p_scalar = voice_master_scalar
    else:
        print("Individual scalars not yet supported")

    voice_p_coll = None
    # Determine if pitch collection will be read in or generated
    # Read the pitch collection in
    if p_coll['mode'] == "READ_FILE":
        print("READ_FILE mode not currently supported for pitch collections")
    # Generate the pitch collection
    elif p_coll['mode'] == "GENERATE":
        print("Attempting to generate pitch collection...")
        mode_specs_param = {'base_multiple':p_coll['base_mult'], "ET_div":p_coll['octave_div'],
                            "mode":"ET"}
        if "scale_mode" in p_coll:
            mode_specs_param['scale_mode'] = p_coll["scale_mode"]
        voice_p_coll = cg.gen_pitch_collection(p_coll['base_pitch'], mode_specs_param)
        # Write pitches to file if option specified
        if p_coll['write_to_file'] != None and p_coll['write_to_file'] == 1:
            util.write_list_to_file(paths['full_folder_path'] + "\\" + voice_id + "pitches_bp" + str(p_coll['base_pitch'])
                                    + "_bm" + str(p_coll['base_mult']) + "_div" + str(p_coll['octave_div']) +
                                    ".txt", voice_p_coll)
            util.write_list_to_collection(paths['full_folder_path'] + "\\" + voice_id + "coll_pitches_bp" +
                                          str(p_coll['base_pitch']) + "_bm" + str(p_coll['base_mult']) + "_div"
                                          + str(p_coll['octave_div']) + ".txt", voice_p_coll)

    # Make the fractals
    voice_raw_fractal = ff.seed_to_raw_fractal(voice_p_seed, piece['pattern_length'], piece['seed_parse_mode'])
    voice_raw_fractal['voice_id'] = voice_id
    voice_pitch_fractal = ff.apply_fractal_to_data(voice_raw_fractal, voice_p_scalar, voice_p_coll, "pitches")
    voice_pitch_fractal['voice_id'] = voice_id
    if 'EOS' in p_instructions:
        voice_pitch_fractal['EOS'] = p_instructions['EOS']
    ff.fractal_to_file(voice_raw_fractal, paths['json_folder_path'])
    pitch_f_path = ff.fractal_to_file(voice_pitch_fractal, paths['json_folder_path'])
    # print("Pitch fractal loc: " + pitch_f_path)

    # Make the score from the pitch fractal
    pitch_res = ff.gen_d_level_fractal(voice_pitch_fractal, piece['depth'])
    pitch_f_filename = pitch_f_path[paths['json_folder_path'].__len__():]
    # print(pitch_f_filename)
    pitch_res_fp = util.write_list_to_collection(
        paths['scores_folder_path'] + pitch_f_filename + "_score_d" + str(piece['depth']) + ".txt",
        pitch_res)

    # Add filepath to max config file variable
    max_config.append(pitch_res_fp)

    return [voice_raw_fractal, voice_pitch_fractal, pitch_f_path, voice_p_seed]


# Parse the indicated duration section, given the correct index from a section of a config file
def process_dur_or_numbers_config(voices, y, seeds, paths, piece, max_config, param_names):
    # VOICE DURATION OR RHYTHM, OR OTHER PARAMETER THAT DEALS WITH NUMBERS ------------------------------

    dur_inst = voices[y][param_names['inst']]
    float_coll = dur_inst[param_names['coll']]
    voice_d_scalar = {}
    # Just take the seed specified by the pitch for now
    voice_d_seed = dur_inst['seed']
    voice_id = "v" + str(y + 1)

    # If the seed for the duration of a voice is set to a number, treat it as a number
    # indicating the seed to use that has been previously mentioned in the file (way to reuse
    # seed without typing it twice)
    if type(voice_d_seed) == int and seeds != None and voice_d_seed <= seeds.__len__():
        voice_p_seed = seeds[voice_d_seed - 1]
    elif type(voice_d_seed) == int and seeds != None and voice_d_seed > seeds.__len__():
        print("Error, seed of index " + str(voice_d_seed) + " is out of bounds. Please fix this error.")
    else:
        seeds.append(voice_d_seed)

    # Set up scalar to be used for this voices duration
    if 'use_master_scalar' in dur_inst and dur_inst['use_master_scalar']:
        voice_d_scalar = voices[y]['master_scalar']
    else:
        voice_d_scalar = dur_inst['scalar']

    # Check for the seed to use
    if type(voice_d_seed) == int and seeds != None and voice_d_seed <= seeds.__len__():
        voice_d_seed = seeds[voice_d_seed - 1]
    elif type(voice_d_seed) == int and seeds != None and voice_d_seed > seeds.__len__():
        print("Error, seed of index " + str(voice_d_seed) + " is out of bounds. Please fix this error.")
    else:
        seeds.append(voice_d_seed)

    voice_d_coll = []
    # Determine if duration collection will be generated or read in
    # Read the duration collection in
    if float_coll['mode'] == "READ_FILE":
        print("READ_FILE mode not currently supported for duration/rhythm collections")
    # Generate the duration collection
    elif float_coll['mode'] == "GENERATE":
        print("Attempting to generate duration collection...")
        voice_d_coll = cg.gen_float_coll(float_coll['method'], float_coll['params'])

    # Write and generate necessary fractals for duration section!
    voice_raw_d_fractal = ff.seed_to_raw_fractal(voice_d_seed, piece['pattern_length'], piece['seed_parse_mode'])
    voice_raw_d_fractal['voice_id'] = voice_id
    voice_dur_fractal = ff.apply_fractal_to_data(voice_raw_d_fractal, voice_d_scalar, voice_d_coll, param_names['name'])
    voice_dur_fractal['voice_id'] = voice_id
    if 'EOS' in dur_inst:
        voice_dur_fractal['EOS'] = dur_inst['EOS']
    ff.fractal_to_file(voice_raw_d_fractal, paths['json_folder_path'])
    dur_f_path = ff.fractal_to_file(voice_dur_fractal, paths['json_folder_path'])

    # GENERATE FRACTALS
    # Now that we have prepared all the data for our voice, save the scores for the voice to a file!

    dur_res = ff.gen_d_level_fractal(voice_dur_fractal, piece['depth'])
    dur_f_filename = dur_f_path[paths['json_folder_path'].__len__():]

    # print(dur_f_filename)
    # print(dur_p_filename)
    # Write scores to file!
    dur_res_fp = util.write_list_to_collection(
        paths['scores_folder_path'] + dur_f_filename + "_score_d" + str(piece['depth']) + ".txt",
        dur_res)

    max_config.append(dur_res_fp)
    return 0


# Read and execute instructions from config file
def parse_and_execute_config_file(filename):
    my_config = ff.read_input_to_var(filename)
    cap = my_config.__len__()

    for x in range(cap):
        cur_piece = my_config[x]
        piece_folder_name = cur_piece['piece_name']
        relative_piece_folder_path = "songs//" + piece_folder_name
        master_pattern_len = cur_piece['pattern_length']
        master_depth = cur_piece['depth']
        paths = {}

        # Create master folder if it does not yet exist
        full_folder_path = util.create_folder_if_dne(relative_piece_folder_path)
        paths['full_folder_path'] = full_folder_path
        print(full_folder_path)
        # Create the path for the max config file
        max_config_path = full_folder_path + "\\" + piece_folder_name + "_max_config.txt"
        print(max_config_path)
        paths['max_config_path'] = max_config_path
        # Create the list that will hold the filepaths needed for the max config file
        max_config_params = []
        # Create all necessary subfolders
        json_folder_path = util.create_folder_if_dne(relative_piece_folder_path + "\\json")
        scores_folder_path = util.create_folder_if_dne(relative_piece_folder_path + "\\scores")
        paths['json_folder_path'] = json_folder_path
        paths['scores_folder_path'] = scores_folder_path

        print("Processing piece '" + piece_folder_name + "'")
        voices = cur_piece['voices']
        voice_cap = voices.__len__()
        # This tells max how many voices the piece will have
        max_config_params.append(str(voice_cap))

        # Store array of seeds used in the piece
        seeds = []

        for y in range(voice_cap):
            print("Processing voice " + str(y + 1))
            # Tells max this is the beginning of a new voice
            max_config_params.append("99NEW_VOICE99")
            voice_id = "v" + str(y + 1)

            # PROCESS PITCH
            # Note* seeds and other vars passed in are modified :)
            p_process_res = process_pitch_config(voices, y, seeds, paths, cur_piece, max_config_params)
            dur_params = {
                "name":"duration",
                "inst":"duration_inst",
                "coll":"duration_coll"
            }
            # PROCESS DURATION
            dur_process_res = process_dur_or_numbers_config(voices, y, seeds, paths, cur_piece, max_config_params,
                                                            dur_params)
            rhythm_params = {
                "name":"rhythm",
                "inst":"rhythm_inst",
                "coll":"rhythm_coll"
            }
            if rhythm_params['inst'] in voices[y]:
                # PROCESS RHYTHM
                rhythm_process_res = process_dur_or_numbers_config(voices, y, seeds, paths, cur_piece, max_config_params,
                                                                   rhythm_params)

            # PROCESS PRESENT RATIO SECTIONS
            ratio_params = {
                "coll":"ratio_coll"
            }
            ratio_sec_present = 1
            rnum = 1
            ratio_process_results = []
            while (ratio_sec_present):
                ratio_params['name'] = "ratio" + str(rnum)
                ratio_params['inst'] = ratio_params['name'] + "_inst"
                if ratio_params['inst'] in voices[y]:
                    ratio_process_results.append(process_dur_or_numbers_config(voices, y, seeds, paths, cur_piece,
                                                                               max_config_params, ratio_params))
                else:
                    ratio_sec_present = 0
                rnum = rnum + 1

        util.write_list_to_collection(max_config_path, max_config_params)
        cap = max_config_params.__len__()
        cur_voice_num = 1
        cur_voice_params = [1, "99NEW_VOICE99"]
        for x in range(2, cap):
            if (x == cap - 1):
                cur_voice_params.append(max_config_params[x])
            if (max_config_params[x] == "99NEW_VOICE99" or x == cap - 1):
                cur_voice_path = full_folder_path + "\\" + piece_folder_name + "_voice" + str(cur_voice_num) + \
                                 "_max_config.txt"
                util.write_list_to_collection(cur_voice_path, cur_voice_params)
                cur_voice_params = [1, "99NEW_VOICE99"]
                cur_voice_num = cur_voice_num + 1
            else:
                cur_voice_params.append(max_config_params[x])




def score():
    depth = 4
    filename = "input"
    my_ext = ".json"
    my_json = ff.read_input_to_var(filename + my_ext)
    res = ff.gen_d_level_fractal(my_json, depth)
    util.write_list_to_collection(osp.curdir + "\\" + filename + "_score_d" + str(depth) + ".txt", res)

def pitch_coll(write_to_file, base_pitch, base_mult, octave_div):
    mode_specs = {}
    mode_specs['mode'] = "ET"
    mode_specs['ET_div'] = octave_div
    mode_specs['base_multiple'] = base_mult
    res = cg.gen_pitch_collection(base_pitch, mode_specs)
    if (write_to_file):
        util.write_list_to_file(osp.curdir + "\\pitches_bp" + str(base_pitch) +
                                 "_bm" + str(base_mult) + "_div" + str(octave_div)
                                + ".txt", res)
        util.write_list_to_collection(osp.curdir + "\\coll_pitches_bp" + str(base_pitch) +
                            "_bm" + str(base_mult) + "_div" + str(octave_div)
                            + ".txt", res)
    return res

def main():
    my_scalar = {'min':0.3, 'max':0.8}
    my_pitch_coll = pitch_coll(WRITE_TRUE, 20, 3, 16)
    raw_fractal = ff.seed_to_raw_fractal("Sammy was acting super silly!", 5)
    pitch_fractal = ff.apply_fractal_to_data(raw_fractal, my_scalar, my_pitch_coll, "pitches")
    pitch_fractal_file_name = ff.fractal_to_file(pitch_fractal, "")
    depth = 5
    res = ff.gen_d_level_fractal(pitch_fractal, depth)
    util.write_list_to_collection(osp.curdir + "\\scores\\" + pitch_fractal_file_name + "_score_d" + str(depth) + ".txt", res)

    dur_coll1 = [50, 60, 70, 90, 100, 110, 120, 140, 150, 160, 170, 180]
    dur_coll2 = []
    for x in range(5, 102):
        dur_coll2.append((x * 2) - 4)
    print(dur_coll2)
    duration_fractal = ff.apply_fractal_to_data(raw_fractal, my_scalar, dur_coll2, "duration")
    duration_res = ff.gen_d_level_fractal(duration_fractal, depth)
    dur_fractal_file_name = ff.fractal_to_file(duration_fractal, "")
    util.write_list_to_collection(osp.curdir + "\\scores\\" + dur_fractal_file_name + "_score_d" + str(depth) + ".txt",
                                  duration_res)


# The new 'main' function. Will parse a config file to create all the specified fractal and pitch data
def new_main():
    parse_and_execute_config_file("input/rando.json")


def gen_12TET():
    pitch_coll(WRITE_TRUE, 27.5, 2, 12)


new_main()
#gen_12TET()

# new_main()
# my_seed = ff.gen_fractal_seed("iohoaihfasdlkfawe")
# my_mid = 5
# ct_low = 0
# ct_hi = 0
# for x in range(1, my_seed.__len__() + 1):
#     my_num = int(my_seed[x-1: x])
#     if my_num < my_mid:
#         ct_low = ct_low + 1
#     else:
#         ct_hi = ct_hi + 1
#
# ct_hi = float(ct_hi)
# ct_low = float(ct_low)
# den = ct_hi + ct_low
# print("High values used: " + str(ct_hi/den * 100.) + "%")
# print("Low values used: " + str(ct_low/den * 100.) + "%")



# print(cg.hgen_ET_pitch_collection(13.75,2,12).__len__())
# print(ff.str_to_hex("059Q"))

# Correlate rhythm with frequencies somehow (in a direct way)
# Correspond with other fx i.e. timbre
# Cliff Calendar (Pieces for player piano); fractal music
# Do set of studies on forms of fractals? i.e. multiple pieces
# Visualize the data! show people the seed
# Consider using raw data

# Prolation / Mensuration canon (but be intentional about it)
#   - Perhaps force into ET or a key signature

# Consider movements! b/c it can be generated easily!

# Consider duration and rhythm as separate
# Structural downbeats (i.e. trigger sound or effect each time sequence returns to beginning)
# Map fractal to timbre, perhaps for params of FM synth
# Revisit pitch coll generation
# perhaps parse out spaces in seed?
# Played at faster speed vs. slower speed
# Next class, bring in max patch + a few example scores :)

#score()
# my_p_coll = pitch_coll(WRITE_TRUE)
# Help with following print protocol from SilentGhost on SO post:
# https://stackoverflow.com/questions/4440516/in-python-is-there-an-elegant-way-to-print-a-list-in-a-custom-format-without-ex
# print('\n'.join('{}: {}'.format(*i) for i in enumerate(my_p_coll)))
# main()
