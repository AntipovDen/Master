threads = 8
file_prefix = "data/dijkstra_edges_equal_vertices"

with open("{}_merged.out".format(file_prefix), 'w') as fout:
    fins = [open("{}_{}.out".format(file_prefix, i + 1), 'r') for i in range(threads)]
    results = [[[float(s) for s in line.split()] for line in fin.readlines()] for fin in fins]
    for f in fins:
        f.close()
    merged = [[sum([results[j][k][i] for j in range(threads)]) / threads for i in range(len(results[0][k]))] for k in range(len(results[0]))]
    for i in merged:
        for j in i:
            fout.write(str(j))
            fout.write(' ')
        fout.write('\n')
