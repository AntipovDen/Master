# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from random import random, randint

# E = 20
# f = 10
# last_delta = 0.0

def gen_deltas(interval, n):
    if n == 1:
        return [interval]
    sep = random() * interval
    return gen_deltas(sep, n // 2) + gen_deltas(interval - sep, n - n // 2)


# def change(data):
#     edge = randint(0, len(data) - 2)
#     l = random() * (data[edge] + data[edge + 1])
#     data[edge] += data[edge + 1] - l
#     data[edge + 1] = l
#
# def update_line(num, data, line):
#     global last_delta
#     last_delta += data[1][-1]
#     print(num, last_delta)
#     change(data[1])
#     line.set_data(data)
#     return line,

# fig = plt.figure()


def run(E, f, deltas):
    deltas_sum = deltas.copy()
    res_e2 = 0
    for i in range(E ** 3):
        edge = randint(1, f)
        l = random()
        if l < (deltas[edge - 1] + deltas[edge]):
            deltas[edge - 1] += deltas[edge] - l
            deltas[edge] = l
        for j in range(f + 1):
            deltas_sum[j] += deltas[j]
        if i == E ** 2:
            res_e2 = deltas_sum.copy()
    return res_e2, deltas_sum

runs = 1000

logfile = open('data/logs/deltas.log', 'w')
for E in [10, 20, 30]:
    for f in [1, E // 2, E - 1]:
        with open('data/experiments/deltas_e{}f{}.out'.format(E, f), 'w') as fout:
            for run_number in range(runs):
                logfile.write('random case, E {} f {} run {}\n'.format(E, f, run_number))
                logfile.flush()
                e2, e3 = run(E, f, gen_deltas(1, f + 1))
                for s in e2:
                    fout.write('{} '.format(s))
                fout.write('\n')
                for s in e3:
                    fout.write('{} '.format(s))
                fout.write('\n')
                fout.flush()
        with open('data/experiments/deltas_worst_e{}f{}.out'.format(E, f), 'w') as fout:
            for run_number in range(runs):
                logfile.write('worst case, E {} f {} run {}\n'.format(E, f, run_number))
                logfile.flush()
                e2, e3 = run(E, f, [1.0] + [0.0] * f)
                for s in e2:
                    fout.write('{} '.format(s))
                fout.write('\n')
                for s in e3:
                    fout.write('{} '.format(s))
                fout.write('\n')
                fout.flush()
logfile.close()

                # animation things

# print(data, sum(data[1]))
# l, = plt.plot([], [], 'bo')
# plt.xlim(0, f)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('delta dinamics')
# line_ani = animation.FuncAnimation(fig, update_line, 1000, fargs=(data, l),
#     interval=100, blit=True)
#
#
# plt.show()