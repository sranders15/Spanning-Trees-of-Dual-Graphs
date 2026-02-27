'''
This file calculates the characteristics of the real data dual graphs
specifically for census tracts and census block groups.

Some of it is based on work in https://github.com/afr13dman/senior-thesis/tree/main/real_graph_exploration, but modified to also compute spanning tree counts

Spanning tree counts are computed using the LU method for determinants, which avoids some computaitonal issues with larger dual graphs, especially the block ones

'''


# import required libraries
import os
from gerrychain import Graph
import re
import pandas as pd
from statistics import median
import networkx as nx
import numpy as np
import scipy
from scipy.sparse.linalg import splu

# Create Definition
def max_degree(G):
    # Initialize max_degree
    max_degree = -1

    # Iterate over all nodes and their degrees
    for degree in G.degree():
        if degree[1] > max_degree:
            max_degree = degree[1]
    
    return max_degree

# assign directory
df_type = 'b' # Work with either tracts (t) or block groups (bg) or blocks (b), though the last option takes a while
directory = "../../local copy of data/" + df_type + '/'
state_vertices = []
i = 0

# iterate over files in that directory
for state_file in os.listdir(directory):
    print(i, ": " , state_file)
    i = i + 1
    f = os.path.join(directory, state_file)

    # check if it is a file
    if os.path.isfile(f):
        # Convert json file to graph object
        state_graph = Graph.from_json(f)

        # Planar?
        planar = nx.check_planarity(state_graph)[0]
        
        # Connected?
        connected = nx.is_connected(state_graph)

        # Calculate avg degree of graph
        avg_degree = 2 * state_graph.number_of_edges() / state_graph.number_of_nodes()

        # Calculate median degree of graph
        degrees = sorted([degree for _, degree in state_graph.degree()], reverse=False)
        median_degree = median(degrees)

        # Calculate max degree
        max_deg = max_degree(state_graph)

        # state and map type
        state = re.search(r"_.*?\.", state_file)
        map_type = re.search(r"^.*?_", state_file)


        
        if connected == True:
            # number of spanning trees
            print("Connected")
            # returns scipy 
            Lap = nx.laplacian_matrix(state_graph)
            # delete last row and column
            T = Lap[:-1, :-1]
       
            # Decompose matrix for better computation
            # Get LU decomposition
            lu = splu(T)
            # For determinant, we only need the diagonal values
            diagL = lu.L.diagonal()
            diagU = lu.U.diagonal()
            # Turn into complex data types for better accuracy
            diagL = diagL.astype(np.complex128)
            diagU = diagU.astype(np.complex128)
            # Calculate log determinant, only take real part 
            # (any complex part should only be computation error)
            # (saw complex part overall much much smaller than real part)
            logabsdet = (np.log(diagL).sum() + np.log(diagU).sum()).real

        else:
            logabsdet = -1
        
        #logabsdet = -1
        state_vertices.append([state.group()[1:-1], map_type.group()[:-1],
                            state_graph.number_of_nodes(), state_graph.number_of_edges(), 
                               planar, connected,
                               avg_degree, median_degree, max_deg, 
                               logabsdet, logabsdet/state_graph.number_of_nodes()])

columns = ['State', 'Map Type', 'Num_vertices', 'Num_edges', 'Planar', 'Connected',
                                            'Avg Degree', 'Median Degree', 'Max Degree', 
                                            'ln_ST', 'ST_const']

# Turn what we have so far into a data frame
df_initial = pd.DataFrame(state_vertices, columns=columns)

# initial entries in new rows
means = [ 'mean', 'bg' ]
medians = [ 'median', 'bg' ]

# caluclate means and medians for numeric columns
for col in ['Num_vertices', 'Num_edges', 'Planar', 'Connected', 'Avg Degree', 'Median Degree', 'Max Degree', 'ln_ST', 'ST_const']:
    # ignore negative numbers for spanning tree count, which are disconnected graphs
    m = np.mean([x for x in df_initial[col] if x >= 0])                       
    means.append(m)
    m = np.median([x for x in df_initial[col] if x >= 0]) 
    medians.append(m)  

state_vertices.append(means)
state_vertices.append(medians)

# Turn list into dataset and save
df = pd.DataFrame(state_vertices, columns=columns)

# Write to file
df.to_csv(f"{df_type}_stats.csv", header=True, index = False)