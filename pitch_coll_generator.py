# Pitch Collection Generator
# Jacques Mathieu - 11/4/18

MAX_PITCH = 20000
MIN_PITCH = 20

# Generate a list that represents a pitch collection in which
# the lowest pitch is the base_pitch, each octave is generated
# from multiplying the base pitch with the base multiple and
# each octave is divided into ET_div equal parts
def gen_pitch_collection(base_pitch, base_multiple, ET_div):
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
            new_pitch = cur_oct_freq * base_multiple**(numerator/ET_div)
            pitch_coll.append(new_pitch)

        cur_oct = cur_oct + 1

    # Put the last octave on the end of the pitch collection
    pitch_coll.append(octaves[last_oct])
    return pitch_coll

