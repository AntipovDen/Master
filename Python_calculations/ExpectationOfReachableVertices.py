__author__ = 'dantipov'

from random import randint
from matplotlib import pyplot as plt
from math import log


def expectations(vertices, max_edges):
    expect = [1] + [0] * (max_edges - 1)
    for edges in range(1, max_edges):
        prev = expect[edges - 1]
        expect[edges] = prev + (prev * (vertices - prev) / vertices) ** 1 / (vertices + 0.08 * edges)
    return expect


def model_graph(vertices, edges):
    reachable = {v : {v} for v in range(vertices)}
    for _ in range(edges):
        v_from, v_to = randint(0, vertices - 1), randint(0, vertices - 1)
        reachable[v_from] = reachable[v_from].union(reachable[v_to])
    return sum([len(reachable[i]) for i in range(vertices)]) / vertices


def modelling_run(vertices, edges, runs):
    print("modelling for", vertices, "vertices and", edges, "edges")
    return sum([model_graph(vertices, edges) for _ in range(runs)]) / runs


vertices = 20
max_edges = 400
edges = [e for e in range(max_edges)]
runs = 100

expect = expectations(vertices, max_edges)
with open('data/reachable_vertices.out', 'r') as f:
    experiment = [float(i) for i in f.readline().split()]


plt.plot(edges, expect, 'bo', edges, experiment, 'ro')
plt.show()
