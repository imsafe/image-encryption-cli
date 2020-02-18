import numpy as np

def convert_dec_to_hex(decimal_number):
    if decimal_number <= 15:
        return "0" + np.base_repr(decimal_number, 16)
    else:
        return np.base_repr(decimal_number, 16)

def sort_second(val):
    return val[1]