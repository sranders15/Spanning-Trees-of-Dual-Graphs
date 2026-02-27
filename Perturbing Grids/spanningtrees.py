# this file contains the following functions:
# decision: used to make a decision with a certain probability p
# makeTriangularLattice: creates a lattice graph and adds all diagonals facing same way
# makeRandomLattice: starts with a lattice graph and adds random diagonal edges
# ST_const: calculates tha "spanning tree constant" of a graph. uses Kirchhoff's Theorem
# graph_from_json: takes a json file and converts it into a graph object


import networkx as nx
import random
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json



def decision(probability):
    return random.random() < probability


def makeTriangularLattice(sidelength):
    # full square/rectangular lattice with all diagonals facing the same way.
    g = nx.grid_graph([sidelength[0],sidelength[1]])
    for i in range(0,sidelength[1]-1):
        for j in range(0,sidelength[0]-1):
            g.add_edge((i,j),(i+1,j+1))
    return g


# random lattice
# make a lattice that is a mix between square and triangular
# lattice will have no crossings, and diagonals can go in either direction

def makeRandomLattice(sidelength,probability):
    g = nx.grid_graph([sidelength[0],sidelength[1]])
    p = probability

    for i in range(0,sidelength[1]-1):
        for j in range(0,sidelength[0]-1):
            # node is the bottom left point of a square
            # with probability p, draw a diagonal in that square
            if decision(p):
                # draw the diagonal
                # direction is chosen 50/50
                if decision(0.5):
                    # draw up right
                    g.add_edge((i,j),(i+1,j+1))
                else:
                    # draw up left
                    g.add_edge((i,j+1),(i+1,j))
    return g

# ST const
def ST_const(graph, forests = False):
    # forests = True means it will calculate spanning FORESTS for disconnected graphs
    # forests = False means it will calculate spanning trees for LARGEST connected component
    if not(forests):
        largest_cc = max(nx.connected_components(graph), key=len)
        graph = graph.subgraph(largest_cc)
    Lap = nx.laplacian_matrix(graph).toarray()
    # remove a row and column
    T = np.delete(Lap,1,0)
    T = np.delete(T,1,1)
    # determinant of T = # of spanning trees
    # we use slogdet to avoid large numbers
    # slogdet computes ln of abs value of det & sign of det
    (sign, logabsdet) = linalg.slogdet(T)
    if sign == 0:
        # i do not know why this happens
        # it has nothing to do with connectivity (?)
        return 0
    else:
        n = graph.number_of_nodes()
        ST = logabsdet/n
        return ST, n

def graph_from_json(json_file):
    # convert json file to graph object
    with open(json_file, 'r') as file:
        data = json.load(file)
    return json_graph.adjacency_graph(data)
