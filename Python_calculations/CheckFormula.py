"""it's a file for checking different fomulas. Usually it doesn't need to be saved"""
from matplotlib import pyplot as plt

__author__ = 'dantipov'

f = open('data/Combinations.dat', 'r')
c = [[float(i) for i in s.split()] for s in [f.readline() for i in range(200)]]
f.close()

def comb(n, k):
    return c[n][min(k, n - k)]

f = open('data/Stirling.dat', 'r')
s = [[float(i) for i in s.split()] for s in [f.readline() for i in range(200)]]
f.close()

phactorial = [1.]
for i in range(1, 200):
    phactorial.append(phactorial[-1] * i)

def stirling(n, k):
    return s[n][k]

n = 100
k = 100

def f(x):
    return sum([comb(n, j) * x ** j * stirling(j, k) for j in range(k, n + 1)])

def f1(x):
    return x ** n * stirling(n, k)

def f2(x):
    return sum([(-1) ** (k - i) * comb(k, i) * (i * x + 1) ** n for i in range(k + 1)]) / phactorial[k]

x = [i / 100 for i in range(1, 80)]
y = [f(x_i) for x_i in x]
y1 = [f1(x_i) for x_i in x]
y2 = [f2(x_i) for x_i in x]
y3 = [y2[i] / y[i] for i in range(79)]

print(y)
print(y1)
print(y2)

plt.plot(x, y3, 'b-') #, x, y2, 'r-')#, x, y2, 'g-')
plt.show()