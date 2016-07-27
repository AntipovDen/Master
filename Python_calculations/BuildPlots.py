__author__ = 'dantipov'

import matplotlib.pyplot as plt
from matplotlib.pylab import savefig




files = []

VE = [(5, 5), (5, 10), (5, 12), (10, 10), (10, 20), (10, 50), (15, 15), (15, 30), (15, 112)]
iterations = [48.98599999999994, 260.6320000000002, 393.9879999999997, 111.0579999999999, 497.91400000000016, 3893.8119999999963, 192.61999999999983, 802.7460000000001, 14507.48200000001]


for ve in VE:
        files.append(open("data/graph_statistics/v" + str(ve[0]) + "e" + str(ve[1]) + ".txt", 'r'))

reachableVertexes = []
unreachableEdges = []
leaves =[]
depthInEdges = []
depthInWeight = []
relaxedEdges = []

for file in files:
    print(file.name)
    reachableVertexes.append([float(i) for i in file.readline().split('\t')[:-1]])
    unreachableEdges.append([float(i) for i in file.readline().split('\t')[:-1]])
    leaves.append([float(i) for i in file.readline().split('\t')[:-1]])
    depthInEdges.append([float(i) for i in file.readline().split('\t')[:-1]])
    depthInWeight.append([float(i) for i in file.readline().split('\t')[:-1]])
    relaxedEdges.append([float(i) for i in file.readline().split('\t')[:-1]])

for j in range(9):
    print(j)
    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(reachableVertexes[j]))], reachableVertexes[j], 'r-',
             [iterations[j], iterations[j]], [0, max(reachableVertexes[j])], 'b-')
    plt.title("reachable vertexes, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/reachable_vertexes_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()

    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(unreachableEdges[j]))], unreachableEdges[j], 'r-',
             [iterations[j], iterations[j]], [0, max(unreachableEdges[j])], 'b-')
    plt.title("unreachable edges, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/unreachable_edges_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()

    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(leaves[j]))], leaves[j], 'r-',
             [iterations[j], iterations[j]], [0, max(leaves[j])], 'b-')
    plt.title("leaves, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/leaves_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()

    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(depthInEdges[j]))], depthInEdges[j], 'r-',
             [iterations[j], iterations[j]], [0, max(depthInEdges[j])], 'b-')
    plt.title("max depth in edges, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/max_depth_e_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()

    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(depthInWeight[j]))], depthInWeight[j], 'r-',
             [iterations[j], iterations[j]], [0, max(depthInWeight[j])], 'b-')
    plt.title("max depth in weight, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/max_depth_w_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()

    plt.figure(1)
    plt.subplot(111)
    plt.plot([i for i in range(len(relaxedEdges[j]))], relaxedEdges[j], 'r-',
             [iterations[j], iterations[j]], [0, max(relaxedEdges[j])], 'b-')
    plt.title("relaxed edges, v=" + str(VE[j][0]) + " e=" + str(VE[j][1]))
    plt.xlabel("iterations")
    plt.xscale('log')
    savefig("data/graph_statistics/plots/relaxed_edges_v" + str(VE[j][0]) + "e" + str(VE[j][1]) + ".png")
    #plt.show()
    plt.clf()
