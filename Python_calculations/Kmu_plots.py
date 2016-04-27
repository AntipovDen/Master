from matplotlib import pyplot as plt
from math import log
from pyx import canvas, path, deco, style, color, text


def make_rarefied_graph():
    with open('../KMU/pic/dijkstra_runtime_merged.out', 'r') as f:
        experiment = [float(s) for s in f.readline().split()]

    gamma = 0.5772156649


    def bound(v, e):
        return e * v * (2 * v - e - 1) / ((e + 1) * (v - e - 1)) * (gamma + log(e)) - e * v * log((v - 1) / (v - e)) / (v - e - 1)

    vertices = list(range(110, 1000, 10))
    plt.plot(vertices, experiment, 'bo', label='experiment')
    plt.plot(vertices, [bound(v, 100) for v in vertices], 'ro', label='theoretical bound')
    plt.xlabel('Vertices')
    plt.ylabel('Iterations')
    plt.title('Runtime for E = 100')
    plt.legend(loc=4)
    plt.show()


def make_picture_for_two_vertices():
    c = canvas.canvas()
    c.stroke(path.rect(0, 0, 12, 1))
    c.stroke(path.rect(1, 0, 1, 1), [style.linewidth.THICK])
    c.stroke(path.rect(5, 0, 1, 1), [style.linewidth.THICK])
    c.stroke(path.rect(7, 0, 1, 1), [style.linewidth.THICK])
    c.stroke(path.rect(10, 0, 1, 1), [style.linewidth.THICK])
    c.stroke(path.line(-0.5, 0.5, -0.5, 6), [deco.earrow(size=0.2)])
    c.stroke(path.line(1.5, 0.5, 1.5, 5), [deco.earrow(size=0.2)])
    c.stroke(path.line(5.5, 0.5, 5.5, 4), [deco.earrow(size=0.2)])
    c.stroke(path.line(7.5, 0.5, 7.5, 3), [deco.earrow(size=0.2)])
    c.stroke(path.line(10.5, 0.5, 10.5, 2), [deco.earrow(size=0.2)])
    c.stroke(path.line(12.5, 0.5, 12.5, 1), [deco.earrow(size=0.2)])
    c.stroke(path.line(5.5, 4, 8, 4), [style.linewidth.THIN])
    c.stroke(path.line(7, 3, 8, 3), [style.linewidth.THIN])
    c.text(7.5, 3.5, r"$\delta_i = l_i - l_{i + 1}$", [text.halign.boxcenter, text.valign.middle])
    c.stroke(path.line(6, 0, 6, -1), [style.linewidth.THIN])
    c.stroke(path.line(7, 0, 7, -1), [style.linewidth.THIN])
    c.text(6.5, -0.4, r"$d_i$", [text.halign.boxcenter, text.valign.middle])
    c.text(-0.5, 3, r"$l_0 = 1.0$", [text.halign.boxleft])
    c.text(5.5, 2.5, r"$l_i$", [text.halign.boxright])
    c.text(7.5, 2, r"$l_{i+1}$", [text.halign.boxleft])
    c.text(12.5, 1.1, r"$l_{E+1} = 0.0$", [text.halign.boxcenter])

    c.writePDFfile("test_picture.pdf")


def make_dense_graph():
    with open('data/experiments/dijkstra_v2_merged.out', 'r') as f:
        experiment = [float(s) for s in f.readline().split()]

    gamma = 0.5772156649

    def theoretical_bound(e):
        return 4 * e ** 2

    def real_bound(e):
        return 4 * e ** 3

    edges = list(range(2, 74, 3))
    plt.plot(edges, experiment, 'bo', label='experiment')
    plt.plot(edges, [theoretical_bound(e) for e in edges], 'ro', label='theoretical bound 4E^2')
    plt.plot(edges, [real_bound(e) for e in edges], 'go', label='seems to be a bound 4E^3')
    plt.xlabel('Edges')
    plt.ylabel('Iterations')
    plt.title('Runtime for V = 2')
    plt.legend(loc=2)
    plt.show()

make_dense_graph()