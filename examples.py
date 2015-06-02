import math
import random

import matplotlib
from matplotlib import pyplot, gridspec
from scipy import stats
from scipy.special import gamma, gammaln

import ternary

## Functions to plot #

def beta(alphas):
    """Multivariate beta function"""
    #return math.exp(sum(map(gammaln, alphas)) - gammaln(sum(alphas)))
    return sum(map(gammaln, alphas)) - gammaln(sum(alphas))

def dirichlet(alphas):
    """Computes Dirichlet probability distribution assuming all parameters alphas > 1."""
    B = beta(alphas)
    def f(x):
        s = 0.
        for i in range(len(alphas)):
            try:
                t = (alphas[i]-1.) * math.log(x[i])
                s += t
            except ValueError:
                return 0.
        return math.exp(s - B)
    return f

def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1.*s

def boundary_and_gridlines(ax=None, scale=30, multiple=5, color="black"):
    ax = ternary.draw_boundary(scale, color=color, ax=ax)
    ternary.draw_gridlines(scale, multiple=multiple, ax=ax, color=color)
    return ax

def various_lines(ax, scale=30):
    ternary.draw_boundary(scale, linewidth=2., color='black', ax=ax)
    ternary.draw_horizontal_line(ax, scale, 16)
    ternary.draw_left_parallel_line(ax, scale, 10, linewidth=2., color='red', linestyle="--")
    ternary.draw_right_parallel_line(ax, scale, 20, linewidth=3., color='blue')
    p1 = ternary.project_point((12,8,10))
    p2 = ternary.project_point((2, 26, 2))
    ternary.draw_line(ax, p1, p2, linewidth=3., marker='s', color='green', linestyle=":")

if __name__ == '__main__':
    ## Boundary and Gridlines
    pyplot.figure()
    scale = 30
    gs = gridspec.GridSpec(1,2)
    ax = pyplot.subplot(gs[0,0])
    boundary_and_gridlines(ax, scale, multiple=5)
    ax.set_title("Simplex Boundary and Gridlines")

    ## Various lines
    ax = pyplot.subplot(gs[0,1])
    various_lines(ax, scale)
    ax.set_title("Various Lines")

    # Scatter Plot
    pyplot.figure()
    scale = 40
    ax = ternary.draw_boundary(scale, color="black")
    ternary.draw_gridlines(scale, multiple=5, ax=ax, color="black")
    points = []
    for i in range(100):
        x = random.randint(1, scale)
        y = random.randint(0, scale - x)
        z = scale - x - y
        points.append((x,y,z))
    ternary.scatter(points, scale=scale)
    ax.set_title("Scatter Plot")

    ## Heatmap roundup
    scale = 60
    for function in [shannon_entropy, dirichlet([4, 8, 13])]:
        pyplot.figure()
        gs = gridspec.GridSpec(2,2)
        ax = pyplot.subplot(gs[0,0])
        ternary.function_heatmap(function, scale=scale, boundary_points=True, ax=ax)
        ternary.draw_boundary(scale+1, ax=ax, color='black')
        ax.set_title("Triangular with Boundary")

        ax = pyplot.subplot(gs[0,1])
        ternary.function_heatmap(function, scale=scale, boundary_points=False, ax=ax)
        ternary.draw_boundary(scale+1, ax=ax, color='black')
        ax.set_title("Triangular without Boundary")

        ax = pyplot.subplot(gs[1,0])
        ternary.function_heatmap(function, scale=scale, boundary_points=True, ax=ax, style="hexagonal")
        ternary.draw_boundary(scale, ax=ax, color='black')
        ax.set_title("Hexagonal with Boundary")

        ax = pyplot.subplot(gs[1,1])
        ternary.function_heatmap(function, scale=scale, boundary_points=False, ax=ax, style="hexagonal")
        ternary.draw_boundary(scale, ax=ax, color='black')
        ax.set_title("Hexagonal without Boundary")

    ## Sample trajectory plot
    pyplot.figure()
    ax = ternary.draw_boundary(color='black')
    ax.set_title("Plotting of sample trajectory data")
    points = []
    with open("curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    ternary.plot(points, linewidth=2.0, ax=ax)

    pyplot.show()

