from matplotlib import pyplot as plt


for v in [50]:#[15, 20, 50]:
    for e in [833]:#[v * 2, v * 5, v ** 2 // 3]:
        runs = 100
        iterations = []
        order_changes = []
        distance_changes = []
        for i in range(1, 5):
            f = open('data/dijkstra_order_changes_v{}e{}_{}.out'.format(v, e, i), 'r')
            for _ in range(runs):
                try:
                    iterations.append(float(f.readline()))
                except ValueError:
                    break
                order_changes += [float(s) for s in f.readline().split()]
                # distance_changes += [float(s) for s in f.readline().split()]
                f.readline()
            f.close()
        order_changes.sort()
        # distance_changes.sort()
        max_iter = max(iterations)
        medium_iter = sum(iterations) / runs
        plt.plot([order_changes[i] for i in range(len(order_changes)) if i % 1000 == 0], [i/runs for i in reversed(range(len(order_changes))) if i % 1000 == 0], 'bo',
                 # order_changes, [i/runs for i in reversed(range(len(order_changes)))], 'b-',
                 [medium_iter], [0], 'ro')
        plt.show()
