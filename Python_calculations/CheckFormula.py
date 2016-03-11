"""it's a file for checking different fomulas. Usually it doesn't need to be saved"""
from math import sqrt, log

from matplotlib import pyplot as plt

for V in [50]:
    for E in [10, 12, 25, 50]:
        max_filename_prefix = "data/experiments/runtime/result-{}-{}-".format(str(V).rjust(3, '0'), str(E).rjust(4, '0'))
        my_filename_prefix = "data/result-{}-{}-".format(str(V).rjust(3, '0'), str(E).rjust(4, '0'))
        for filename_suffix in [str(i).rjust(3, '0') + '.txt' for i in [V // 2, V, V * 2]]:
            with open(max_filename_prefix + filename_suffix, 'r') as f:
                print(f.readline().split()[-1])
            with open(my_filename_prefix + filename_suffix, 'r') as f:
                print(f.readline().split()[-1])
            print()