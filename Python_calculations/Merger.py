threads = 8
file_prefix = "data/simplified_runtime"

with open("{}_merged.out".format(file_prefix), 'w') as fout:
    fins = [open("{}_{}.out".format(file_prefix, i + 1), 'r') for i in range(threads)]
    results = [[float(s) for s in fin.readline().split()] for fin in fins]
    for f in fins:
        f.close()
    merged = [sum([results[j][i] for j in range(threads)]) / threads for i in range(len(results[0]))]
    for i in merged:
        fout.write(str(i))
        fout.write(' ')