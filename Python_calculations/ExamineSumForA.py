from math import isnan

__author__ = 'dantipov'

V = 20

with open('data/Combinations.dat', 'r') as f:
    c = [[int(i) for i in s.split()] for s in [f.readline() for j in range(V ** 2 + 1)]]



with open('data/a.out', 'r') as f:
    a = []
    for v in range(V + 1):
        a.append([])
        for i in range(v):
            a[-1].append([[[0] * V ** 2]])
            for l in range(1, v - i + 1):
                a[-1][-1].append([int(i) for i in f.readline().split()])

with open('data/s.out') as f:
    s = []
    for v in range(V + 1):
        s.append([])
        for l in range(v + 1):
            s[-1].append([])
            for m in range(v - l + 1):
                s[-1][-1].append([int(i) for i in f.readline().split()])


print('i\'ve read everything')


def check_summands(v, i, l, e, file):
    table = [[0] * (e - l + 1) for _ in range(v - l - i + 1)]
    for m in range(1, v - l - i + 2):
        for e_s in range(l, e + 1):
            table[m - 1][e_s - l] = a[v-l][i-1][m][e-e_s] * c[e][e_s] * c[V - v + l][l] * s[v][l][m][e_s - l] / a[v][i][l][e] * 100
    for row in table:
        for elem in row:
            file.write(format(elem, '.2f').ljust(7))
        file.write(str(sum(row)) + '\n')
    for e_s in range(e - l + 1):
        file.write(format(sum([table[m][e_s] for m in range(v - l - i + 1)]), '.2f').ljust(7))


with open('data/a_summands.out') as f:
    for v in range(1, V + 1):
        for i in range(v):
            for l in range(1, v - i + 1):
                for e in range(V ** 2):
                    check_summands(v, i, l, e, f)



