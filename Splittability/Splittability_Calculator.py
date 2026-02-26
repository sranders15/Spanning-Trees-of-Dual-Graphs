### Splittability Calculator
### Calculate splittability rates

import networkx as nx
import json
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque
import os
import json
import pandas as pd
import time
import sys

from splittability_functions import WilsonsAlgorithm, GraphPartitioner, run_partition_simulationsss

# Set Parameters to Calculate Success Rate
geog = sys.argv[1]
abbr = sys.argv[2]
p = 2  # Number of partitions
k = 178  # Number of successful splits to target


# Read in dual graph
base_dir = "../local copy of data/" + geog + "/"

# read in graph
file_path = os.path.join(base_dir, f'{geog}_{abbr}.json')
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
        graph = json_graph.adjacency_graph(data)
        print(f"Loaded graph for {abbr.upper()} with {len(graph)} nodes.")
except FileNotFoundError:
    print(f"File not found for {abbr.upper()}: {file_path}")
except Exception as e:
    print(f"Error loading {abbr.upper()}: {e}")

# If graph is disconnected: Only use largest connected component
if not nx.is_connected(graph):
    Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
    G0 = graph.subgraph(Gcc[0])

graph = G0


print(f"\nRunning simulations for {abbr.upper()}")
try:
    start_time = time.time()
    trials, success_rate = run_partition_simulationsss(graph, p, k)
    end_time = time.time() 

    print(f"{abbr.upper()}: Took {trials} trials → Success Rate: {success_rate:.2f}%")
    print(f"Compute time: {end_time-start_time} seconds")
    new_row = {'Geography':[geog], 
                'State':[abbr], 
                'Num Vertices': len(graph.nodes()), 
                'Partitions':[p], 
                'Trials':[trials], 
                'Success Rate':[success_rate/100], 
                'Time': [(end_time-start_time)] }
    new_row_df = pd.DataFrame(new_row)
    new_row_df.to_csv(geog + str(k) + '_results.csv', mode='a', index=False, header=False)
except Exception as e:
    print(f"Error running partition simulations for {abbr.upper()}: {e}")