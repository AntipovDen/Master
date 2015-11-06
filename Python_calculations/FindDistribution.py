__author__ = 'dantipov'

from math import e, atan2, pi, erf, log, sqrt
from matplotlib import pyplot as plt
from  scipy.special import gammaincc, gammainc, betainc, beta
from functools import reduce
from numpy import sum

def gammaDistribution(k, theta): #best result with k = 8, theta = 23 (k beetween 5 and 10)
    def f(x):
        return gammainc(k, x/theta)
    return f

def puassonDistribution(lamb):
    def f(x):
        return gammaincc(x + 1, lamb)
    return f

def betaDistribution(a, b):
    def f(x):
        return betainc(a, b, x)
    return f

def weibullDistribution(k, lamb):
    def f(x):
        return 1 - e ** (- (x / lamb) ** k)
    return f

f = open("data/distribution.txt")

def lognormalDistribution(u, sig):
    def f(x):
        return 0.5 * erf((log(x) - u) / sqrt(2) / sig) + 0.5
    return f


def myDistribution():
    N = 100
    def p(M):
        p_ = [1 - (1 - 1 / (N ** 2)) ** M]
        for i in range(2, min(N, M + 1)):
            # p_.append(reduce(lambda x, y: x * y, [1 - i for i in p_]) * (1 - (1 - p_[-1] / (N ** 2) * (N - 1)) ** M))
            p_.append((1 - sum(p_)) * (1 - (1 - p_[-1] / (N ** 2) * (N - 1)) ** M))
        # return 1 - reduce(lambda x, y: x * y, [1 - i for i in p_])
        return sum(p_)
    def f(x):
        return p(x) * (N - 1)
    return f


x = [i for i in range(1, 501)]
y = [float(i) for i in f.readline().split(',')[1:]]
y1 = [myDistribution()(i) for i in range(1, 501)]
plt.plot(x, y, 'bo', label='original')
plt.plot(x, y1, 'ro', label='assumption')
plt.legend(loc='lower right')
plt.show()


# x = [i for i in range(1, 501)]
# y = [float(i) for i in f.readline().split(',')[1:]]
# y1 = [100 * lognormalDistribution(5.2, 0.4)(i) for i in range(1, 501)]
# y2 = [100 * lognormalDistribution(0, 0.38)(i/180) for i in range(1,501)]
#
# plt.plot(x, y, 'bo', label='original')
# plt.plot(x, y1, 'ro', label='k = 2, lambda = 200')
# plt.plot(x, y2, 'go', label='k = 5, lambda = 200')
# plt.legend(loc='lower right')
# plt.show()

# x = [i for i in range(501)]
# y = [float(i) for i in f.readline().split(',')]
# y1 = [100 * weibullDistribution(2, 200)(i) for i in range(501)]
# y2 = [100 * weibullDistribution(5, 200)(i) for i in range(501)]
#
# plt.plot(x, y, 'bo', label='original')
# plt.plot(x, y1, 'ro', label='k = 2, lambda = 200')
# plt.plot(x, y2, 'go', label='k = 5, lambda = 200')
# plt.legend(loc='lower right')
# plt.show()

# x = [i for i in range(501)]
# y = [float(i) for i in f.readline().split(',')]
# y1 = [100 * betaDistribution(10, 5)(i/501) for i in range(501)]
# y2 = [100 * betaDistribution(6, 11)(i/501) for i in range(501)]
#
# plt.plot(x, y, 'bo', label='original')
# plt.plot(x, y1, 'ro', label='alpha = 10, beta = 5')
# plt.plot(x, y2, 'go', label='alpha = 6, beta = 11')
# plt.legend(loc='lower right')
# plt.show()
#
#
# x = [i for i in range(501)]
# y = [float(i) for i in f.readline().split(',')]
# y1 = [100 * puassonDistribution(10)(i/19) for i in range(501)]
# y2 = [100 * puassonDistribution(4)(i/50) for i in range(501)]
#
# plt.plot(x, y, 'bo', label='original')
# plt.plot(x, y1, 'ro', label='lambda = 10, extension = 19')
# plt.plot(x, y2, 'go', label='lambda = 4, extension = 50')
# plt.legend(loc='lower right')
# plt.show()
#
# y1 = [100 * gammaDistribution(3, 60)(i) for i in range(501)]
# y2 = [100 * gammaDistribution(8, 23)(i) for i in range(501)]
#
# plt.plot(x, y, 'bo', label='original')
# plt.plot(x, y1, 'ro', label='k = 3, theta = 60')
# plt.plot(x, y2, 'go', label='k = 8, theta = 23')
# plt.legend(loc='lower right')
# plt.show()

