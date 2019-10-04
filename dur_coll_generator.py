# Duration Collection Generator
# Jacques Mathieu - 11/19/18

MAX_DUR = 5000.0
MIN_DUR = 5.0

def gen_dur_coll(method, params):
    if method == "asc":
        return gen_asc_dur_coll(params)

def gen_asc_dur_coll(params):
    base_dur = params['base_dur']
    max_dur = params['max_dur']
    if base_dur < MIN_DUR:
        base_dur = MIN_DUR
    if max_dur > MAX_DUR:
        max_dur = MAX_DUR
    dur_coll = []
    iter = params['iter']
    cur_num = base_dur
    while (cur_num < max_dur):
        dur_coll.append(cur_num)
        cur_num = cur_num + iter

    return dur_coll