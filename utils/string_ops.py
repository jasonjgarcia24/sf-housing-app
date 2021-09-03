import re


def line_break_split(s, w):
    if not w:
        return s

    prev_str = s
    blanks   = [_.start() for _ in re.finditer(" ", prev_str)]
    str_len  = len(prev_str)

    breaks  = []
    br      = 0
    new_str = ""

    for s, e in zip([0] + blanks, blanks + [str_len]):
        if e - br > w:
            breaks.append((br, s))
            new_str += f"{prev_str[breaks[-1][0]:breaks[-1][-1]]}<br>"     
            br = s+1
            
    breaks.append((br, str_len))
    new_str += f"{prev_str[breaks[-1][0]:breaks[-1][-1]]}"     
    
    return new_str