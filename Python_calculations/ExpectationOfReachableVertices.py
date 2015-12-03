__author__ = 'dantipov'

from random import randint
from matplotlib import pyplot as plt
from scipy.special import gammainc
from math import log

def expectations(vertices, max_edges):
    expect = [1] + [0] * (max_edges - 1)
    for edges in range(1, max_edges):
        prev = expect[edges - 1]
        expect[edges] = prev + (prev * (vertices - prev) / (vertices ** 1.5 + edges))  #/ (vertices)
    return expect


def model_graph(vertices, edges):
    reachable = [{v} for v in range(vertices)]
    for _ in range(edges):
        v_from, v_to = randint(0, vertices - 1), randint(0, vertices - 1)
        reachable[v_from] = reachable[v_from].union(reachable[v_to])
        for v in range(vertices):
            if v_from in reachable[v]:
                reachable[v] = reachable[v].union(reachable[v_to])
    return sum([len(reachable[i]) for i in range(vertices)]) / vertices


def modelling_run(vertices, edges, runs):
    print("modelling for", vertices, "vertices and", edges, "edges")
    return sum([model_graph(vertices, edges) for _ in range(runs)]) / runs


# just experiments
# with open('data/reachable_vertices.out', 'w') as f:
#     runs = 5000
#     for vertices in range(5, 6):
#         f.write(" ".join([str(modelling_run(vertices, edges, runs)) for edges in range(vertices ** 2 + 1)]))
#         f.write('\n')
#         f.flush()
# exit(0)

vertices = 20
max_edges = 401
edges = [e for e in range(max_edges)]

expect = expectations(vertices, max_edges)

with open('data/reachable_vertices20.out', 'r') as f:
   experiment = [float(i) for i in f.readlines()[-1].split()]

# addendnum = [experiment[i] * (vertices - experiment[i]) / (experiment[i + 1] - experiment[i]) for i in edges[:-1]]

difference = [experiment[i + 1] - experiment[i] for i in range(max_edges - 1)]
expected_defferences = [expect[i + 1] - expect[i] for i in range(max_edges - 1)]



plt.plot(experiment[:-1], difference, 'ro', expect[:-1], expected_defferences, 'bo')
#plt.plot(edges, expect, 'bo', edges, experiment[:max_edges], 'ro')
plt.show()
