threads = 8
file_prefix = "dijkstra_v2"

with open("{}_merged.out".format(file_prefix), 'w') as fout:
    fins = [open("{}_{}.out".format(file_prefix, i + 1), 'r') for i in range(threads)]
    # results = [[[float(s) for s in line.split()] for line in fin.readlines()] for fin in fins]
    results = [[float(s) for s in fin.readlines()[:24]] for fin in fins]
    for f in fins:
        f.close()
    # merged = [[sum([results[j][k][i] for j in range(threads)]) / threads for i in range(len(results[0][k]))] for k in range(len(results[0]) -1 )]
    merged = [sum([results[i][j] for i in range(threads)])/threads for j in range(24)]
    for i in merged:
        fout.write('{} '.format(i))
    # it's uncommon
    # merged.append([])
    # for i in range(5):
    #     merged[-1].append(sum([results[j][-1][i] for j in range(threads) if len(results[j][-1]) > i]) / max(sum([1 for j in range(threads) if len(results[j][-1]) > i]), 1))
    # for i in merged:
    #     for j in i:
    #         fout.write(str(j))
    #         fout.write(' ')
    #     fout.write('\n')
