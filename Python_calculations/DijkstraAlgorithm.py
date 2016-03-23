import sys

__author__ = 'Den'

# from math import sqrt, ceil
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

    relaxed = set()

    cur_vertex = vertices[0]
    answer = []
    while True :
        for edge in graph[cur_vertex.number]:
            relaxValue = cur_vertex.mark + edge.weight

            if vertices[edge.to].mark > relaxValue:
                vertices[edge.to].mark = relaxValue
                relaxed.add((cur_vertex.number, edge.to, edge.weight))

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
def init_graph(v, e, max_weight,):
    return [(randrange(v), randrange(v), randrange(max_weight)) for _ in range(e)]


def mutate(v, e, max_weight):
    e[randrange(len(e))] = (randrange(v), randrange(v), randrange(max_weight))


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


# EA run
# now it opimizes only with mutating edgges that are not in the connected components into the edges
# that lead from connected component out of it
def evo_run(vertices, edges, max_weight):
    global logfile, run_number
    run_number += 1
    logfile.write("Run number {}\n".format(run_number))
    logfile.flush()
    if vertices > 2 * edges:
        algorithm = dijkstra_many_vertices
    else:
        algorithm = dijkstra
    graph = init_graph(vertices, edges, max_weight)
    f = 0
    iterations = 0
    while f != edges:
        nextGen = graph.copy()
        mutate(vertices, nextGen, max_weight)
        relaxed = algorithm(vertices, nextGen)

        if relaxed >= f:
            if relaxed > f:
                logfile.write("relaxed: {} with {} iterations\n".format(relaxed, iterations))
                logfile.flush()
            graph = nextGen
            f = relaxed
        iterations += 1

    return iterations


def optimize_simple(vertices, edges, max_weight):
    # global run_number
    # print("Run: ", run_number)
    # run_number += 1
    graph = init_graph(edges, max_weight)
    f = 0
    iterations = 0
    current_connected_component = {0}
    # no_change_iterations = 0
    while f != edges:
        # if no_change_iterations > 1000000:
        #     exit(0)
        iterations += 1
        # nextGen = graph.copy()

        # mutation with lower probability
        edge_number = randrange(edges)
        v_from = randrange(vertices)
        v_to = randrange(vertices)
        if graph[edge_number][0] not in current_connected_component and v_from in current_connected_component and v_to not in current_connected_component:
            graph[edge_number] = (v_from, v_to, max_weight)
            current_connected_component.add(v_to)
            f += 1
        #     no_change_iterations = 0
        # else:
        #     no_change_iterations += 1

    return iterations

if len(sys.argv) == 1:
    stream_number = ''
else:
    stream_number = '_' + sys.argv[1]
logfile = open("data/logs/dijkstra_edges_equal_vertices{}.log".format(stream_number), 'w')
runs = 10
with open('data/dijkstra_edges_equal_vertices{}.out'.format(stream_number), 'w') as f:
    for e in [100, 500, 1000]:
        for vertices in [e, e + 1, e + 2, e + 5, e + 10, e + 20]:
            for max_weight in [2, e // 2, e, e + 20, 2 * e]: # range(edges + 10, 10 * edges, 10):
                run_number = 0
                logfile.write("V{}E{}W{}\n".format(vertices, e, max_weight))
                logfile.flush()
                res = sum([evo_run(vertices, e, max_weight) for _ in range(runs)]) / runs
                f.write(str(res) + ' ')
                f.flush()
            f.write('\n')
            f.flush()
logfile.close()


