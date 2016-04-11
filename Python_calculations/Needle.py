from random import randrange as rr, random
from numpy.random import choice


def mutate(x, i):
    to_change = choice([n for n in range(len(x))], i, False)
    x_ret = x.copy()
    for n in to_change:
        x_ret[n] = 1 - x_ret[n]
    return x_ret


def run(n):

    ans = [rr(0, 2) for _ in range(n)]
    x_0 = [rr(0, 2) for _ in range(n)]
    if x_0 == ans:
        return 1
    iterations = 1
    x_1 = [1 - x_i for x_i in x_0]
    while x_1 != ans:
        r = random()
        distance = min([i for i in range(1, n) if prob[i] >= r])
        x_1 = mutate(x_0, distance)
        iterations += 1
    return iterations


runs = 10000
for n in range(1, 50):
    print("Processing {}".format(n))
    comb = [1] + [comb[i] + comb[i + 1] for i in range(n - 1)] + [1]
    prob = [0]
    m = 2 ** n - 2
    for i in range(1, n):
        prob.append(prob[-1] + comb[i] / m)
    print(sum([run(n) for _ in range(runs)]) / runs)

