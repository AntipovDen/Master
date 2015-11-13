__author__ = 'dantipov'

c_prev = [1]
c_new = []

with open('data/Combinations.dat', 'w') as f:
    f.write('1\n')
    for n in range(1, 5001):
        c_new = [0] * (n + 1)
        c_new[0] = c_new[-1] = 1
        f.write('1 ')
        for k in range(1, n):
            c_new[k] = c_prev[k - 1] + c_prev[k]
            f.write(str(c_new[k]) + ' ')
        f.write('1\n')
        c_prev = c_new