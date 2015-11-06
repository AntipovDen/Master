__author__ = 'dantipov'

from igraph import *
from random import randint
from matplotlib import pyplot as plt

def rand(N):
    return randint(0, N - 1)


def graphResults(N, M):
    g = Graph().as_directed()
    g.add_vertices(N)
    g.add_edges([(rand(N), rand(N)) for i in range(M)])

    bfs = g.bfs(0)
    res = [bfs[1][i + 1] - bfs[1][i] for i in range(1, len(bfs[1]) - 1)]
    if bfs[0][-1] != 0:
        res.append(N - bfs[1][-1])
    res += [0] * (N - len(bfs[1]) + 1)

    # print(g)
    # print(res)
    # g.vs["label"] = [i for i in range(N)]
    # plot(g, layout = g.layout_kamada_kawai())

    return res


runs = 500
N = 20

results = []
# for i in range(N - 1):
#     results.append([])

for M in range(N ** 2):
    print(M)
    res = [0] * (N - 1)
    for i in range(runs):
        newRes = graphResults(N, M)
        res = [res[i] + newRes[i] for i in range(N - 1)]
    res = [r/runs for r in res]
    # for i in range(N - 1):
    #     results[i].append(res[i])
    results.append(res)

x = [i for i in range(N ** 2)]
y = [sum(r) for r in results]
plt.plot(x, y, 'b-')
plt.show()

# f = open("data/bfs_1.txt", 'w')
# for res in results:
#     for i in res:
#         f.write(str(i))
#         f.write(' ')
#     f.write('\n')
