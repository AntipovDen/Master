from numpy import sum
import matplotlib.pyplot as plt

__author__ = 'dantipov'


def variation(i, k, v, e):
    res = ((1 - ((v - 1) / v) ** 2) / e) ** k
    for j in range(i - 2 * k + 2, i + 1):
        res *= j
    return res


def r(i, v, e):
    f = open("data/v" + str(v) + "e" + str(e) + ".txt")
    return float(f.readline().split("\t")[i])


def expectation(i, v, e):
    return sum([(v / (v - 1)) ** (4 * k) * variation(i, k, v, e) * (i - 2 * k) for k in range((i + 1) // 2)]) * r(i, v, e) * ((v - 1) / v) ** (2 * (i - 1)) / v
    # return sum([r(i, v, e) / (v ** 2) * ((v - 1) / v) ** (2 * (i - 1)) * ((e - 1) / e) ** (j - 1) for j in range(1, i)])


y = [expectation(i, 15, 15) for i in range(1, 200)]
x = [i for i in range(1, 200)]

plt.plot(x, y, 'r-')
plt.xlabel('iterations')
plt.ylabel('leaves')
plt.show()
