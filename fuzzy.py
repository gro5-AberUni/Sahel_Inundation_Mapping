import numpy as np
import numba
from numba import jit

#@jit(nopython=True)
def fuzzy_gt(data:np.array, low_bound:float, up_bound:float)->np.array:
    fuzzy_out = (data - low_bound) * 1/(up_bound-low_bound)
    #fuzzy_out[data < low_bound] = 0
    fuzzy_out = np.where(data < low_bound,0,fuzzy_out)
    #fuzzy_out[data > up_bound] = 1
    fuzzy_out = np.where(data > up_bound, 1, fuzzy_out)
    return fuzzy_out

#@jit(nopython=True)
def fuzzy_lt(data:np.array, low_bound:float, up_bound:float)->np.array:
    fuzzy_out = (data - up_bound) * 1/(low_bound-up_bound)
    #fuzzy_out[data < low_bound] = 1
    fuzzy_out = np.where(data < low_bound, 1, fuzzy_out)
    #fuzzy_out[data > up_bound] = 0
    fuzzy_out = np.where(data > up_bound, 0, fuzzy_out)
    return fuzzy_out

##@jit(nopython=True)
def fuzzy_and(fuzzy_lst:list[np.array])->np.array:
    tmp_stack = np.stack(fuzzy_lst)
    return np.min(tmp_stack, axis=0)

##@jit(nopython=True)
def fuzzy_or(fuzzy_lst:list[np.array])->np.array:
    tmp_stack = np.stack(fuzzy_lst)
    return np.max(tmp_stack, axis=0)


