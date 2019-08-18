# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 22:19:51 2018

@author: shen1994
"""

import pickle
import numpy as np


def load_pair_vector(pkl_path):
    pkl_file = open(pkl_path, "rb")
    big_number, size, v_number = pickle.load(pkl_file)
    x_1 = []
    for _ in range(int(big_number / size)):
        x_1.extend(list(pickle.load(pkl_file)))
    x_1 = np.asarray(x_1, dtype="float32")
    pkl_file.close()
    return x_1, big_number


