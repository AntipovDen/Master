__author__ = 'dantipov'

from matplotlib import pyplot as plt
from matplotlib.pylab import savefig

e1 = [[float(i) for i in s.split(' ')[:-1]] for s in open("data/e.out").readlines()]
e = [[]]

last = 0;
vg = 0

while (last != len(e1)):
    vg += 1
    e.append([])
    for eg in range(vg ** 2 + 1):
        e[vg].append(e1[last]);
        last += 1
        if last == len(e1):
            break

y = [0] * 200
for i in range(20):
    x = [j for j in range(1, 201)]
    y = [e[20][j][i] + y[j] for j in range(200)]
    plt.figure(1)
    plt.subplot(111)
    plt.plot(x, y, 'bo')
    plt.title("reachable vertices, v = 20, max depth =" + str(i))
    plt.xlabel("edges")
    plt.ylabel("reachable vertices")
    savefig("data/reachable_i_le" + str(i) + ".png")
    plt.clf()

for i in range(1, 21):
    for j in range(0, i ** 2 + 1):
        print(i, j, e[i][j])


