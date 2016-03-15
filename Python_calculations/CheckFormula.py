"""it's a file for checking different fomulas. Usually it doesn't need to be saved"""
from math import sqrt, log

from matplotlib import pyplot as plt

gamma = 0.5772156649

def runtime(e, v):
    return e * v * (2 * v - e - 1) / ((e + 1) * (v - e - 1)) * (gamma + log(e)) - e * v / (v - e - 1) * log((v - 1) / (v - e))

with open("data/experiments/simplified_runtime_merged.out", 'r') as f:
    experiments = [float(s) for s in f.readline().split()]

e = 100
checkpoints = list(range(e + 10, e * 10, 10))
assumption = [runtime(100, v) for v in checkpoints]

plt.plot(checkpoints, experiments, 'ro', checkpoints, assumption, 'bo')
plt.show()