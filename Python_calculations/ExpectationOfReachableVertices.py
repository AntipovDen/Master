__author__ = 'dantipov'

from random import randint
from matplotlib import pyplot as plt
from scipy.special import gammainc
from math import log


def get_expectations(vertices, max_edges):
    expect = [1] + [0] * (max_edges - 1)
    for edges in range(1, max_edges):
        prev = expect[edges - 1]
        expect[edges] = prev + prev * (vertices - prev) ** 2 / vertices ** 3 * (1 + 1/vertices) ** edges
    return expect


def get_experiment(filename, max_edges):
    with open(filename, 'r') as f:
        return [float(i) for i in f.readline().split()[:max_edges]]


def get_experiments(filename):
    with open(filename, 'r') as f:
        return [[] for _ in range(5)] + [[float(v) for v in s.split()] for s in f.readlines()]


def get_differences(distribution):
    return [distribution[i + 1] - distribution[i] for i in range(len(distribution) - 1)]


# this is how experiments were done

# def model_graph(vertices, edges):
#     reachable = [{v} for v in range(vertices)]
#     for _ in range(edges):
#         v_from, v_to = randint(0, vertices - 1), randint(0, vertices - 1)
#         reachable[v_from] = reachable[v_from].union(reachable[v_to])
#         for v in range(vertices):
#             if v_from in reachable[v]:
#                 reachable[v] = reachable[v].union(reachable[v_to])
#     return sum([len(reachable[i]) for i in range(vertices)]) / vertices
#
#
# def modelling_run(vertices, edges, runs):
#     print("modelling for", vertices, "vertices and", edges, "edges")
#     return sum([model_graph(vertices, edges) for _ in range(runs)]) / runs



experiments = get_experiments('data/reachable_vertices50.out')
print(experiments)
for v in range(5, 27):
    max_edges = len(experiments[v]) // 2
    edges = list(range(max_edges))
    expect = get_expectations(v, max_edges)
    experiment = experiments[v][:max_edges]

    p2 = [(experiment[e + 1] - experiment[e]) * v ** 3 / (experiment[e] * (v - experiment[e]) ** 2) for e in edges[:-1]]
    plt.plot(edges[:-1], p2, 'bo', edges[:-1], [(1 + 1/v) ** e for e in edges[:-1]], 'r-')
    plt.show()


vertices = 50
max_edges = 400
edges = [e for e in range(max_edges)]

expect = get_expectations(vertices, max_edges)
experiment = get_experiment('data/reachable_vertices50.out', max_edges)

# expected_dif = get_differences(expect)
# experiment_dif = get_differences(experiment)



# # show experiment and expected distributions
plt.plot(edges, experiment, 'ro', edges, expect, 'bo')
plt.show()
#
# # # show differences depending of number of edges in graph
# plt.plot(edges[:-1], experiment_dif, 'ro', edges[:-1], expected_dif, 'bo')
# plt.show()
#
#
# # show differences depending of number of number of reachable vertices
# plt.plot(experiment[:-1], experiment_dif, 'ro', expect[:-1], expected_dif, 'bo')
# plt.show()

# assumption: expected_dif[i] = experiment[i] * (vertices - experiment[i]) * smth. let's find smth!
# assume = [experiment[i] * (vertices - experiment[i]) / vertices ** 2 for i in range(max_edges - 1)]
# assumption = [experiment_dif[i] / assume[i] for i in range(max_edges - 1)]
# plt.plot(edges[:-1], assumption, 'ro') #, edges[:-1], expected_dif, 'bo')
# plt.show()
# plt.plot(experiment[:-1], assumption, 'ro')#, expect[:-1], expected_dif, 'bo')
# plt.show()