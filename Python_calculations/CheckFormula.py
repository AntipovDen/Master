"""it's a file for checking different fomulas. Usually it doesn't need to be saved"""
from math import sqrt, log, pi

from matplotlib import pyplot as plt

gamma = 0.5772156649

def runtime(e, v):
    return (2 + e / (v - e)) * v * (log(e) + gamma)
    # if e == v - 1:
    #     return 2 * e * (log(e) + gamma) + (pi * e) ** 2 / 6
    # return e * v * (2 * v - e - 1) / ((e + 1) * (v - e - 1)) * (gamma + log(e)) - e * v / (v - e - 1) * log((v - 1) / (v - e))

with open("data/experiments/dijkstra_edges_equal_vertices_merged.out", 'r') as f:
    experiments = {100: {}, 500: {}, 1000: {}}
    for e in [100, 500]:
        for v in [e, e + 1, e + 2, e + 5, e + 10, e + 20]:
            experiments[e][v] = {}
            results = [float(i) for i in f.readline().split()]
            lengths = [2, e // 2, e, e + 20, 2 * e]
            for i in range(5):
                experiments[e][v][lengths[i]] = results[i]
    for e in [1000]:
        for v in [e, e + 1]:
            experiments[e][v] = {}
            results = [float(i) for i in f.readline().split()]
            lengths = [2, e // 2, e, e + 20, 2 * e]
            for i in range(5):
                experiments[e][v][lengths[i]] = results[i]

for e in [100, 500]:
    vertices = [e, e + 1, e + 2, e + 5, e + 10, e + 20]
    plt.plot(vertices[1:], [runtime(e, v) for v in vertices[1:]], 'b-',
             vertices, [experiments[e][v][2] for v in vertices], 'go',
             vertices, [experiments[e][v][e // 2] for v in vertices], 'ro',
             vertices, [experiments[e][v][e] for v in vertices], 'co',
             vertices, [experiments[e][v][e + 20] for v in vertices], 'yo',
             vertices, [experiments[e][v][2 * e] for v in vertices], 'ko',)
    plt.show()

for e in [1000]:
    vertices = [e, e + 1]
    plt.plot(vertices[1:], [runtime(e, v) for v in vertices[1:]], 'bo',
             vertices, [experiments[e][v][2] for v in vertices], 'go',
             vertices, [experiments[e][v][e // 2] for v in vertices], 'ro',
             vertices, [experiments[e][v][e] for v in vertices], 'co',
             vertices, [experiments[e][v][e + 20] for v in vertices], 'yo',
             vertices, [experiments[e][v][2 * e] for v in vertices], 'ko',)
    plt.show()
