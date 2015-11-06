__author__ = 'Den'

import random
from math import sqrt, ceil
from matplotlib import pyplot as plt

#Graph edge class
class Edge:
    def __init__(self, targetVertex, weight):
        self.to = targetVertex
        self.weight = weight

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

#pop the min element from the heap and edit references to heap
def pop(heap, placeInHeap):
    if len(heap) == 1:
        return heap.pop()
    res = heap[0]
    placeInHeap[res.number] = -1
    heap[0] = heap.pop()
    placeInHeap[heap[0].number] = 0
    cur = 0;
    while (cur + 1) * 2 < len(heap):
        next2 = (cur + 1) * 2
        next1 = next2 - 1
        if next2 < len(heap):
            if heap[next1] < heap[next2]:
                if heap[cur] > heap[next1]:
                    heap[cur], heap[next1] = heap[next1], heap[cur]
                    placeInHeap[heap[cur].number] = cur
                    placeInHeap[heap[next1].number] = next1
                    cur = next1
                else:
                    break
            else:
                if heap[cur] > heap[next2]:
                    heap[cur], heap[next2] = heap[next2], heap[cur]
                    placeInHeap[heap[cur].number] = cur
                    placeInHeap[heap[next2].number] = next2
                    cur = next2
                else:
                    break
        else:
            if heap[cur] > heap[next1]:
                heap[cur], heap[next1] = heap[next1], heap[cur]
                placeInHeap[heap[cur].number] = cur
                placeInHeap[heap[next1].number] = next1
                cur = next1
            else:
                break
    return res

#relax the vertex in the heap
def relax(heap, placeInHeap, vertexNum, relaxValue):
    curV = placeInHeap[vertexNum]
    heap[curV].mark = relaxValue
    while curV > 0 and heap[curV] < heap[curV // 2]:
        heap[curV], heap[curV // 2] = heap[curV // 2], heap[curV]
        placeInHeap[heap[curV].number] = curV
        placeInHeap[heap[curV // 2].number] = curV // 2

#this function takes number of vertexes and array of edges in format (vFrom, vTo, weight)
#and returns number of relaxed edges and the distance from the start vertex
def dijkstra(v, edges):
    graph = [[] for i in range(v)]

    for edge in edges:
        graph[edge[0]].append(Edge(edge[1], edge[2]))

    #array of vertexes marks
    marks = [0] + [float('inf')] * (v - 1)
    #heap of vertexes. On each step of algorithm we pop the vertex
    # with minimal mark and decrease keys of all relaxed vertexes
    heap = [Vertex(float('inf'), i) for i in range(v)]
    heap[0].mark = 0
    #link to the vertex in the heap
    placeInHeap = [i for i in range(v)]

    #number of relaxed edges
    relaxed = 0
    maxMark = 0
    #algorithm step;
    while heap and heap[0] != float('inf'):
        curV = pop(heap, placeInHeap).number

        for edge in graph[curV]:
            relaxValue = marks[curV] + edge.weight

            if marks[edge.to] > relaxValue:
                marks[edge.to] = relaxValue
                if placeInHeap[edge.to] != -1:
                    relax(heap, placeInHeap, edge.to, relaxValue)
                relaxed += 1

    for mark in marks:
        if mark != float('inf') and mark > maxMark:
            maxMark = mark

    return [maxMark, relaxed];


#operations for EA testing
def initGraph(e, maxWeight):
    return [(1, 0, maxWeight)] * e

def mutate(edges, vertexes, maxWeight):
    edges[random.randrange(len(edges))] = (random.randrange(vertexes), random.randrange(vertexes), random.randrange(maxWeight))

#function take statistics about the graph:
#1) number of vertexes that are reachable from the start vertex
#2) number of edges that couldn't be reached from the start vertex
#   but were mutated before
#3) number of leaves
#4) the max depth  in the graph

def statistics(v, edges, maxWeight):
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
    leaves = 0 #number of vertexes with only one input edge and no output edges

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


#EA run
def optimize(vertexes, edges, maxWeight):
    graph = initGraph(edges, maxWeight)
    f = 0
    results = []
    iterations = 0
    while f != edges:
        nextGen = graph.copy()
        mutate(nextGen, vertexes, maxWeight)
        result = dijkstra(vertexes, nextGen)
        relaxed = result[1]
        if relaxed >= f:
            graph = nextGen
            f = relaxed
#            results.append(statistics(vertexes, graph, maxWeight) + result)
#        else:
#            results.append(results[-1])
        iterations += 1

    return iterations


f = open('const_edges_2.out', 'w')
runs = 500
e = [10, 20, 30]
maxWeight = 15
results = []
for E in e:
    results.append([])
    f.write(str(E))
    f.write(' ')
    f.flush()
    for V in range(E // 2, E + 2):
        print('V:', V)
        results[-1].append(0)
        for i in range(runs):
            results[-1][-1] += optimize(V, E, maxWeight) / runs
        f.write(str(results[-1][-1]))
        f.write(' ')
        f.flush()
    print(E, 'ended')
    f.write('\n')

plt.plot([V for V in range(e[0] // 2, e[0] + 2)], results[0], 'b-', label='10 edges')
plt.plot([V for V in range(e[1] // 2, e[1] + 2)], results[1], 'r-', label='20 edges')
plt.plot([V for V in range(e[2] // 2, e[2] + 2)], results[2], 'g-', label='30 edges')
plt.xlabel("Vertices")
plt.ylabel("Iterations")
plt.legend(loc=2)
plt.show()

# f = open("data/const_vertexes_2.txt", 'w')
# runs = 500
# v = [5, 10,15]
# maxWeight = 15
# results = []
# for V in v:
#     results.append([])
#     f.write(str(V))
#     f.write(' ')
#     f.flush()
#     for E in range(V, V ** 2 // 2, (V // 5)): #range(V, V ** 2 // 2, 3):
#         print('E:', E)
#         results[-1].append(0)
#         for i in range(runs):
#             results[-1][-1] += optimize(V, E, maxWeight) / runs
#         f.write(str(results[-1][-1]))
#         f.write(' ')
#         f.flush()
#     print(V, 'ended')
#     f.write('\n')
#
# plt.plot([E for E in range(v[0], v[0] ** 2 // 2, 1)], results[0], 'b-', label='5 verticies')
# plt.plot([E for E in range(v[1], v[1] ** 2 // 2, 2)], results[1], 'r-', label='10 verticies')
# plt.plot([E for E in range(v[2], v[2] ** 2 // 2, 3)], results[2], 'g-', label='15 verticies')
# plt.xlabel("Edges")
# plt.ylabel("Iterations")
# plt.legend(loc=2)
# plt.show()

exit(0)

def average(x, y, proportion):
    return list(map(lambda a, b: (a * proportion + b) / (proportion + 1), x, y))

def mergeResults(results, curResults, weights):
    for i in range(min(len(results), len(curResults))):
        results[i] = average(results[i], curResults[i], weights[i])
        weights[i] += 1

    for i in range(len(results), len(curResults)):
        results.append(curResults[i])
        weights.append(1)


for V in [5, 10, 15]:
    for E in [V, 2 * V, V ** 2 // 2]:
        print("V:", V, 'E:', E);
        runs = 2000
        results = []
        weights = []
        f = open("data/v" + str(V) + "e" + str(E) + "_1.txt", 'w')
        for run in range(runs):
            mergeResults(results, optimize(V, E, V), weights);

        for res in results:
            f.write(str(res[0]))
            f.write('\t')
        f.write('\n')
        for res in results:
            f.write(str(res[1]))
            f.write('\t')
        f.write('\n')
        for res in results:
            f.write(str(res[2]))
            f.write('\t')
        f.write('\n')
        for res in results:
            f.write(str(res[3]))
            f.write('\t')
        f.write('\n')
        for res in results:
            f.write(str(res[4]))
            f.write('\t')
        f.write('\n')
        for res in results:
            f.write(str(res[5]))
            f.write('\t')
        f.write('\n')