__author__ = 'dantipov'

runs = 1000
# this is the fastest way to calculate combinations
c_prev = [1]
c_new = []
for n in range(runs):
    c_new.append(n + 1)
    c_new.append(1)
    for k in range(1, n):
        c_new[k] = c_prev[k] + c_prev[k - 1]
    c_new, c_prew = c_prev, c_new

