import sys

__author__ = 'Den'

# from math import sqrt, ceil
# from matplotlib import pyplot as plt
from random import randrange, random


# Graph edge class
class Edge:
    def __init__(self, targetVertex, weight):
        self.to = targetVertex
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight >= other.weight

# Vertex class that is comparable by the distance to it that is kept in the "mark" field
class Vertex:
    def __init__(self, mark, number):
        self.mark = mark
        self.number = number

    def __lt__(self, other):
        return self.mark < other.mark

    def __le__(self, other):
        return self.mark <= other.mark

    def __gt__(self, other):
        return self.mark > other.mark

    def __ge__(self, other):
        return self.mark >= other.mark


# this function takes number of vertices and array of edges in format (vFrom, vTo, weight)
# and returns number of relaxed edges
def dijkstra_many_vertices(v, edges):
    graph = {}
    left_vertices = set()
    vertices = {}
    for edge in edges:
        if edge[0] != -1:
            if edge[0] in graph:
                graph[edge[0]].append(Edge(edge[1], edge[2]))
            else:
                graph[edge[0]] = [Edge(edge[1], edge[2])]
            left_vertices.add(edge[1])
            if edge[1] not in vertices:
                vertices[edge[1]] = Vertex(float('inf'), edge[1])


        vertices[0] = Vertex(0., 0)

    relaxed = 0

    cur_vertex = vertices[0]
    while True:
        if cur_vertex.number in graph:
            for edge in graph[cur_vertex.number]:
                relaxValue = cur_vertex.mark + edge.weight

                if vertices[edge.to].mark > relaxValue:
                    vertices[edge.to].mark = relaxValue
                    relaxed += 1

        if len(left_vertices) > 0:
            cur_vertex = min([vertices[i] for i in left_vertices])
            left_vertices.remove(cur_vertex.number)
            if cur_vertex.mark == float('inf'):
                break
        else:
            break

    return relaxed


def dijkstra(v, edges):
    graph = [[] for _ in range(v)]
    for edge in edges:
        if edge[0] != -1:
            graph[edge[0]].append(Edge(edge[1], edge[2]))

    vertices = [Vertex(0., 0)] + [Vertex(float('inf'), i) for i in range(1, v)]
    left_vertices = {i for i in range(1, v)}

    relaxed = 0

    cur_vertex = vertices[0]
    answer = []
    while True:
        graph[cur_vertex.number].sort()
        for edge in graph[cur_vertex.number]:
            relaxValue = cur_vertex.mark + edge.weight

            if vertices[edge.to].mark > relaxValue:
                vertices[edge.to].mark = relaxValue
                relaxed += 1  # .add((cur_vertex.number, edge.to, edge.weight))

        answer.append(cur_vertex)
        if len(left_vertices) > 0:
            cur_vertex = min([vertices[i] for i in left_vertices])
            left_vertices.remove(cur_vertex.number)
            if cur_vertex.mark == float('inf'):
                break
        else:
            break

    return relaxed, answer


# operations for EA
def init_graph(v, e):
    return [(randrange(v), randrange(v), random()) for _ in range(e)]


def mutate(v, e):
    e[randrange(len(e))] = (randrange(v), randrange(v), random())



# EA run
# now it opimizes only with mutating edgges that are not in the connected components into the edges
# that lead from connected component out of it
def evo_run(vertices, edges):
    global logfile, run_number
    run_number += 1
    logfile.write("Run number {}\n".format(run_number))
    logfile.flush()
    # if vertices > 2 * edges:
    #     algorithm = dijkstra_many_vertices
    # else:
    algorithm = dijkstra
    graph = init_graph(vertices, edges)
    f = 0
    iterations = 0
    results = []
    while f != edges:
        nextGen = graph.copy()
        mutate(vertices, nextGen)
        relaxed, answer = algorithm(vertices, nextGen)

        if relaxed >= f:
            if relaxed > f:
                logfile.write("relaxed: {} with {} iterations\n".format(relaxed, iterations))
                logfile.flush()
            if len(results) == 0 or results[-1][1] != answer:
                results.append((iterations, relaxed, answer))
            graph = nextGen
            f = relaxed
        iterations += 1

    return results


def optimize_simple(vertices, edges, max_weight):
    # global run_number
    # print("Run: ", run_number)
    # run_number += 1
    graph = init_graph(edges, max_weight)
    f = 0
    iterations = 0
    current_connected_component = {0}
    while f != edges:
        iterations += 1

        # mutation with lower probability
        edge_number = randrange(edges)
        v_from = randrange(vertices)
        v_to = randrange(vertices)
        if graph[edge_number][0] not in current_connected_component and v_from in current_connected_component and v_to not in current_connected_component:
            graph[edge_number] = (v_from, v_to, max_weight)
            current_connected_component.add(v_to)
            f += 1

    return iterations

if len(sys.argv) == 1:
    stream_number = ''
else:
    stream_number = '_' + sys.argv[1]
logfile = open("data/logs/dijkstra_distance_dynamics{}.log".format(stream_number), 'w')
runs = 10
run_number = 0
with open('data/dijkstra_distance_dynamics{}.out'.format(stream_number), 'w') as f:
    e = 150
    v = 30
    for _ in range(runs):
        results = evo_run(v, e)
        for i in range(1, len(results)):
            iterations, fitness, cur_res = results[i]
            prev_res = results[i-1][2]
            if len(cur_res) != len(prev_res):
                if len(cur_res) > len(prev_res):
                    res = '+{}'.format(len(cur_res) - len(prev_res))
                else:
                    res = str(len(cur_res) - len(prev_res))
                print(res)
            else:
                res = sum([abs(results[i][1][j] - results[i-1][1][j]) for j in range(len(results[i][1]))])
            f.write("iterations: {} fitness: {} res: {}\n".format(str(results[i][0]).ljust(6), str(results[i][2]).ljust(2), res))
            f.flush()
logfile.close()


