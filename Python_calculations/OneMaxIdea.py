__author__ = 'dantipov'

from random import random, randint
from matplotlib import pyplot as plt
from math import log

n = 20


def f(x):
    return sum(x)


def flip(x, flips, allowed_to_flip):
    flipped = [0] * n
    flippables = sum(allowed_to_flip)
    for i in range(flips):
        to_flip = randint(0, flippables)
        j = allowed_to_flip.index(1)
        for k in range(to_flip - 1):
            j += 1
            while not allowed_to_flip[j]:
                j += 1
        x[j] = 1 - x[j]
        allowed_to_flip[j] = 0
        flipped[j] = 1
        flippables -= 1
    return flipped


def mutate(x, flipped, res):
    f1 = flip(x, (n - res) // 2, [1 - i for i in flipped])
    f2 = flip(x, (n - res) // 2, flipped.copy())
    for i in range(n):
        flipped[i] = f1[i] or f2[i]


calls = 0


def opt(x, flipped, unflipped, max_res, cur_res):
    global calls
    if max_res == cur_res:
        return
    x1 = x.copy()
    x1_flipped = flip(x1, (max_res - cur_res) // 2, flipped.copy())
    x1_unflipped = [flipped[i] - x1_flipped[i] for i in range(n)]
    opt(x1, x1_flipped, x1_unflipped, (cur_res + max_res) // 2, f(x1))
    x2 = x.copy()
    x2_flipped = flip(x2, (max_res - cur_res) // 2, unflipped.copy())
    x2_unflipped = [unflipped[i] - x2_flipped[i] for i in range(n)]
    opt(x2, x2_flipped, x2_unflipped, (cur_res + max_res) // 2, f(x2))
    for i in range(n):
        if flipped[i]:
            x[i] = x1[i]
        elif unflipped[i]:
            x[i] = x2[i]
    calls += 2


def run():
    x = [randint(0, 1) for _ in range(n)]
    flipped = [0] * n
    cur_res = f(x)

    iters = 1
    if cur_res != n:
        flipped = flip(x, n - cur_res, [1] * n)
        iters = 2
        cur_res = f(x)

    while cur_res < n:
        x_copy = x.copy()
        flipped_copy = flipped.copy()

        mutate(x, flipped, cur_res)
        new_res = f(x)
        if new_res > cur_res:
            cur_res = new_res
        else:
            x = x_copy
            flipped = flipped_copy
        iters += 1

    return iters


def run1():
    global calls
    x = [randint(0, 1) for _ in range(n)]
    cur_res = f(x)
    calls = 1
    if cur_res < n:
        flipped = flip(x, n - cur_res, [1] * n)
        cur_res = f(x)
        calls = 2
        if cur_res < n:
            opt(x, flipped, [1 - i for i in flipped], n, cur_res)
    return calls

runs = 100
#print(sum([run1() for r in range(runs)]))


res = []
ns = [i for i in range(5, 1000)]

with open("data/my_one_max_solution.out", 'r') as file:
    plt.plot(ns, [float(i) for i in file.readline().split()], 'bo', ns, [1.2 * i for i in ns], 'r-')
plt.show()