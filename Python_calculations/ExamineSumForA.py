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
    max_cell = max_row = max_col = 0
    for m in range(1, v - l - i + 2):
        for e_s in range(l, e + 1):
            table[m - 1][e_s - l] = a[v-l][i-1][m][e-e_s] * c[e][e_s] * c[V - v + l][l] * s[v][l][m][e_s - l] / a[v][i][l][e] * 100
            max_cell = max(table[m - 1][e_s - l], max_cell)
    for row in table:
        for elem in row:
            file.write(format(elem, '.2f').ljust(7))
        row_sum = sum(row)
        file.write(str(row_sum) + '\n')
        max_row = max(row_sum, max_row)
    for e_s in range(e - l + 1):
        col_sum = sum([table[m][e_s] for m in range(v - l - i + 1)])
        file.write(format(col_sum, '.2f').ljust(7))
        max_col = max(col_sum, max_col)
    return max_cell, max_row, max_col



max_max_cell = max_max_row = max_max_col = 0
min_max_cell = min_max_row = min_max_col = 100
with open('data/a_summands.out', 'w') as f:
    for v in range(1, V + 1):
        for i in range(1, v):
            for l in range(1, v - i + 1):
                for e in range(V ** 2):
                    if a[v][i][l][e] > 0.:
                        cur_max_cell, cur_max_row, cur_max_col = check_summands(v, i, l, e, f)
                        max_max_cell = max(max_max_cell, cur_max_cell)
                        max_max_row = max(max_max_row, cur_max_row)
                        max_max_col = max(max_max_col, cur_max_col)
                        min_max_cell = min(min_max_cell, cur_max_cell)
                        min_max_row = min(min_max_row, cur_max_row)
                        min_max_col = min(min_max_col, cur_max_col)

with open('data/max_min_summands.out', 'w') as f:
    f.write(str(max_max_cell) + ' ' + str(max_max_row) + ' ' + str(max_max_col) + '\n')
    f.write(str(min_max_cell) + ' ' + str(min_max_row) + ' ' + str(min_max_col) + '\n')
