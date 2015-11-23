__author__ = 'dantipov'


max_row_numbers = [[]]
V = 20

with open('data/max_row.out', 'r') as f:
    for vg in range(1, V + 1):
        max_row_numbers.append([[], []])
        for v in range(2, vg + 1):
            max_row_numbers[vg].append([[]])
            for i in range(1, v):
                max_row_numbers[vg][v].append([[]])
                for l in range(1, v - i + 1):
                    max_row_numbers[vg][v][i].append([int(i) for i in f.readline().split()])

def is_monotone(arr):
    prev_max = -1
    for i in range(len(arr)):
        if arr[i] < prev_max - 1:
            return False
        elif arr[i] > prev_max:
            prev_max = arr[i]
    return True



max_row_of_V_e = [[[-2] * V for j in range(V ** 2 + 1)] for i in range(V + 1)]

for vg in range(1, V + 1):
    for v in range(2, vg + 1):
        for i in range(1, v):
            for l in range(1, v - i + 1):
                for e in range(l, vg ** 2 + 1):
                    cur = max_row_numbers[vg][v][i][l][e - l]
                    if (max_row_of_V_e[vg][e][v - i - l] == -2):
                        max_row_of_V_e[vg][e][v - i - l] = cur
                    elif (cur != max_row_of_V_e[vg][e][v - i - l]):
                        print(vg, v, i, l , e)



