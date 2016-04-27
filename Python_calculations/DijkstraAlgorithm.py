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
    # answer = []
    while True:
        # graph[cur_vertex.number].sort()
        for edge in graph[cur_vertex.number]:
            relaxValue = cur_vertex.mark + edge.weight

            if vertices[edge.to].mark > relaxValue:
                vertices[edge.to].mark = relaxValue
                relaxed += 1  # .add((cur_vertex.number, edge.to, edge.weight))

        # answer.append(cur_vertex)
        if len(left_vertices) > 0:
            cur_vertex = min([vertices[i] for i in left_vertices])
            left_vertices.remove(cur_vertex.number)
            if cur_vertex.mark == float('inf'):
                break
        else:
            break

    return relaxed  # , answer


# operations for EA
def init_graph(v, e):
    return [(randrange(v), randrange(v), random()) for _ in range(e)]


def mutate(v, e):
    e[randrange(len(e))] = (randrange(v), randrange(v), random())



# EA run

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
    # cur_order = [Vertex(0, i) for i in range(vertices)]
    # order_changes = []
    # distances_changes = []
    while f != edges:
        iterations += 1
        next_gen = graph.copy()
        mutate(vertices, next_gen)
        relaxed = algorithm(vertices, next_gen)

        if relaxed >= f:
            if relaxed > f:
                logfile.write("relaxed: {} with {} iterations\n".format(relaxed, iterations))
                logfile.flush()
            # order_changed, distances_changed = False, False
            # for i in range(min(len(answer), len(cur_order))):
            #     if not order_changed and cur_order[i].number != answer[i].number:
            #         order_changed = True
            #         order_changes.append(iterations)
            #     if not distances_changed and cur_order[i].mark != answer[i].mark:
            #         distances_changed = True
            #         distances_changes.append(iterations)
            #     if distances_changed and order_changed:
            #         break

            graph = next_gen
            f = relaxed

    return iterations  # , order_changes, distances_changes


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


v = 2
if len(sys.argv) == 1:
    stream_number = ''
else:
    stream_number = '_{}'.format(sys.argv[1])
logfile = open("data/logs/dijkstra_v2{}.log".format(stream_number), 'w')
runs = 10
run_number = 0
with open('data/experiments/dijkstra_v2{}.out'.format(stream_number), 'w') as f:
    for e in list(range(2, 100, 3)):
        f.write('{}\n'.format(sum([evo_run(v, e) for _ in range(runs)]) / runs))
        f.flush()
        # for _ in range(runs):
        #     iterations, order_changes, distances_changes = evo_run(v, e)
        #     f.write(str(iterations) + '\n')
        #     for iter in order_changes:
        #         #i'll merge them later
        #         f.write(str(iter) + ' ')
        #     f.write('\n')
        #     for iter in distances_changes:
        #         #i'll merge them later
        #         f.write(str(iter) + ' ')
        #     f.write('\n')
        #     f.flush()
logfile.close()


