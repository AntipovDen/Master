__author__ = 'Den'

import random
from math import sqrt, ceil
# from matplotlib import pyplot as plt
from random import randrange


# Graph edge class
class Edge:
    def __init__(self, targetVertex, weight):
        self.to = targetVertex
        self.weight = weight


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
def dijkstra(v, edges):
    graph = [[] for i in range(v)]
    for edge in edges:
        if edge[0] != -1:
            graph[edge[0]].append(Edge(edge[1], edge[2]))

    vertices = [Vertex(0., 0)] + [Vertex(float('inf'), i) for i in range(1, v)]
    left_vertices = {i for i in range(1, v)}

    relaxed = 0

    cur_vertex = Vertex(0., 0)
    while True :
        for edge in graph[cur_vertex.number]:
            relaxValue = cur_vertex.mark + edge.weight

            if vertices[edge.to] > relaxValue:
                vertices[edge.to] = relaxValue
                relaxed += 1

        if len(left_vertices) > 0:
            cur_vertex = min([vertices[i] for i in left_vertices])
            left_vertices.remove(cur_vertex)
            if cur_vertex.mark == float('inf'):
                break
        else:
            break

    return relaxed


# operations for EA
def init_graph(e, max_weight):
    return [(-1, -1, max_weight)] * e


def mutate(edges, vertices, max_weight):
    edges[randrange(len(edges))] = (randrange(vertices), randrange(vertices), randrange(max_weight))


# function take statistics about the graph:
# 1) number of vertices that are reachable from the start vertex
# 2) number of edges that couldn't be reached from the start vertex
#    but were mutated before
# 3) number of leaves
# 4) the max depth  in the graph
def statistics(v, edges, maxWeight):  #TODO: check the current statistics and modify them
    graph = [[] for i in range(v)]

    for edge in edges:
        graph[edge[0]].append(Edge(edge[1], edge[2]))

    depthes = [0] + [v] * (v - 1)
    bfsQueue = [0]

    while len(bfsQueue) > 0:
        i = bfsQueue.pop(0)
        for edge in graph[i]:
            j = edge.to
            if depthes[j] > depthes[i] + 1:
                depthes[j] = depthes[i] + 1
                bfsQueue.append(j)

    reachable = 0
    depth = 0
    for i in range(v):
        if depthes[i] < v:
            reachable += 1
            if depthes[i] >= depth:
                depth = depthes[i]

    unreachableEdges = 0 # all edges - edges 1->0 - edges, reached by bfs
    leaves = 0 #number of vertices with only one input edge and no output edges

    inputEdges = [0] * v
    outputEdges = [0] * v
    for edge in edges:
        inputEdges[edge[1]] += 1
        outputEdges[edge[0]] += 2
        if (depthes[edge[0]] == v and (edge[0] != 1 or edge[1] != 0 or edge[2] != maxWeight)):
            unreachableEdges += 1
    for i in range(v):
        if (inputEdges[i] == 1 and outputEdges[i] == 0 and depthes[i] != v):
            leaves += 1

    return [reachable, unreachableEdges, leaves, depth]



run_number = 0
# EA run
# now it opimizes only with mutating edgges that are not in the connected components into the edges
# that lead from connected component out of it
def optimize(vertices, edges, max_weight):
    global run_number
    print("Run: ", run_number)
    run_number += 1
    graph = init_graph(edges, max_weight)
    f = 0
    iterations = 0
    while f != edges:
        nextGen = graph.copy()
        mutate(nextGen, vertices, max_weight)
        relaxed = dijkstra(vertices, nextGen)

        if relaxed >= f:
            graph = nextGen
            f = relaxed
        iterations += 1

    return iterations

def optimize_simple(vertices, edges):
    global run_number
    print("Run: ", run_number)
    run_number += 1
    graph = init_graph(edges, 1)
    f = 0
    iterations = 0
    current_connected_component = {0}
    no_change_iterations = 0
    while f != edges:
        if no_change_iterations > 1000000:
            print(f)
            print(current_connected_component)
            print([e for e in graph if e[0] in current_connected_component])
            exit(0)
        iterations += 1
        # nextGen = graph.copy()

        # mutation with lower probability
        edge_number = randrange(edges)
        v_from = randrange(vertices)
        v_to = randrange(vertices)
        if graph[edge_number][0] not in current_connected_component and v_from in current_connected_component and v_to not in current_connected_component:
            graph[edge_number] = (v_from, v_to, 1)
            current_connected_component.add(v_to)
            f += 1
            no_change_iterations = 0
        else:
            no_change_iterations += 1
        # mutate(nextGen, vertices, maxWeight)
        # relaxed = dijkstra(vertices, nextGen)

        # if relaxed >= f:
        #     graph = nextGen
        #     f = relaxed
        #
    return iterations

# here we can do some
def optimize_simple2(vertices, edges):
    global run_number
    print("Run: ", run_number)
    run_number += 1
    graph = init_graph(edges, 1)
    f = 0
    iterations = 0
    current_connected_component = {0}
    no_change_iterations = 0
    while f != edges:
        if no_change_iterations > 1000000:
            print(f)
            print(current_connected_component)
            print([e for e in graph if e[0] in current_connected_component])
            exit(0)
        iterations += 1
        # nextGen = graph.copy()

        # mutation with lower probability
        edge_number = randrange(edges)
        v_from = randrange(vertices)
        v_to = randrange(vertices)
        if graph[edge_number][0] not in current_connected_component and v_from in current_connected_component and v_to not in current_connected_component:
            graph[edge_number] = (v_from, v_to, 1)
            current_connected_component.add(v_to)
            f += 1
            no_change_iterations = 0
        else:
            no_change_iterations += 1
        # mutate(nextGen, vertices, maxWeight)
        # relaxed = dijkstra(vertices, nextGen)

        # if relaxed >= f:
        #     graph = nextGen
        #     f = relaxed
        #
    return iterations

edges = 1000
vertices = list(range(edges + 100, 10 * edges, 10))
runs = 100

medium_iterations = [sum([optimize_simple(v, edges) for _ in range(runs)]) / runs for v in vertices]

with open("dijkstra_simple.out", 'w') as f:
    for i in medium_iterations:
        f.write(str(i) + ' ')

