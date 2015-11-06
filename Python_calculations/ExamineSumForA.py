__author__ = 'dantipov'

V = 20

with open('data/Combinations.dat', 'r') as f:
    c = [[int(i) for i in s.split()] for s in [f.readline() for j in range(V ** 2 + 1)]]


def comb(n, k):
    return c[n][min(k, n - k)]


f = open('data/a.out', 'r')
a = []
for v in range(V + 1):
    a.append([])
    for i in range(v):
        a[-1].append([[[0] * V ** 2]])
        for l in range(1, v - i + 1):
            a[-1][-1].append([float(i) for i in f.readline().split()])



