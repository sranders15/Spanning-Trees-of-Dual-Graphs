# Graph Visualizations
# Adapted from ../num_spanning_trees.py to change some colors/labels and also include blocks
# The code in ../num_spanning_trees.py was originally written by Sara Anderson

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set colors and labels
cl = ['b', 'r', 'g']
q = ['t', 'bg', 'b']
color_map = {'t': 'red', 'bg': 'blue', 'b':'g'}

# Read in data: tracts, block groups, and blocks
t = pd.read_csv("t_stats.csv")
bg = pd.read_csv("bg_stats.csv")
b = pd.read_csv("b_stats.csv")

# select only relevant columns
t_trees = t[["Map Type", 'Num_vertices', 'ln_ST', 'ST_const']]
bg_trees = bg[["Map Type", 'Num_vertices', 'ln_ST', 'ST_const']]
b_trees = b[["Map Type", 'Num_vertices', 'ln_ST', 'ST_const']]

# combine into one list for easy looping
# also, only keep those states that have at least one spanning tree
# we previously set ln_ST to 0 if the graph had no spanning trees (e.g. if it's not connected)
trees = [t_trees[t_trees['ln_ST'] > 0], bg_trees[bg_trees['ln_ST'] > 0], b_trees[b_trees['ln_ST'] > 0]]

# plot st constant v num of nodes for t, bg, and b
plt.figure()
for p in [0, 1,2]:
    plt.scatter(trees[p]['Num_vertices'], trees[p]['ST_const'], color = cl[p], label = q[p])
plt.title('Spanning Tree Constant vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('Spanning Tree Constant')
plt.legend(loc="lower right")
plt.savefig('t_bg_b_nodes_stconst.png')

# plot st constant v ln(num of nodes) for t, bg, and b
# Thought this might help us see things better
plt.figure()
for p in [0, 1,2]:
    plt.scatter([np.log(x) for x in trees[p]['Num_vertices']], trees[p]['ST_const'], color = cl[p], label = q[p])
plt.title('Spanning Tree Constant vs Number of Nodes')
plt.xlabel('ln(Number of Nodes)')
plt.ylabel('Spanning Tree Constant')
plt.legend(loc="lower right")
plt.savefig('t_bg_b_lnnodes_stconst.png')

# plot st constant v num of nodes just for t and bg
plt.figure()
for p in [0, 1]:
    plt.scatter(trees[p]['Num_vertices'], trees[p]['ST_const'], color = cl[p], label = q[p])
plt.title('Spanning Tree Constant vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('Spanning Tree Constant')
plt.legend(loc="lower right")
plt.savefig('t_bg_nodes_stconst.png')


# plot log of span trees v num of nodes for t, bg, and b
trend = []
line = []
st = [[],[],[]]
plt.figure()
for p in [0, 1,2]:
    trend = np.polyfit(trees[p]['Num_vertices'], trees[p]['ln_ST'], 1)
    line = np.poly1d(trend)
    plt.scatter(trees[p]['Num_vertices'], trees[p]['ln_ST'], c = cl[p], label = q[p], alpha=0.5)
    plt.plot(trees[p]['Num_vertices'], line(trees[p]['Num_vertices']), 'k')
    # display eq of line to four digits
    st[p] = 'y = ' + str(trend[0])[0:4] + 'x + ' + str(trend[1])[0:4]
plt.title('ln(Number of Spanning Trees) vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('ln(Number Spanning Trees)')
y_max = max([max(trees[0]['ln_ST']), max(trees[1]['ln_ST']), max(trees[2]['ln_ST'])] )
x_max = max([max(trees[1]['Num_vertices']), max(trees[0]['Num_vertices']), max(trees[2]['Num_vertices'])])
plt.text(x_max * 0.75, y_max * 0, st[0], c = cl[0])
plt.text(x_max * 0.75, y_max * 0.1, st[1], c = cl[1])
plt.text(x_max * 0.75, y_max * 0.2, st[2], c = cl[2])
plt.legend()
plt.savefig('t_bg_b_nodes_lnst.png')

# plot log of span trees v num of nodes for t, bg
trend = []
line = []
st = [[],[]]
plt.figure()
for p in [0, 1]:
    trend = np.polyfit(trees[p]['Num_vertices'], trees[p]['ln_ST'], 1)
    line = np.poly1d(trend)
    plt.scatter(trees[p]['Num_vertices'], trees[p]['ln_ST'], c = cl[p], label = q[p], alpha=0.5)
    plt.plot(trees[p]['Num_vertices'], line(trees[p]['Num_vertices']), 'k')
    # display eq of line to four digits
    st[p] = 'y = ' + str(trend[0])[0:4] + 'x + ' + str(trend[1])[0:4]
plt.title('ln(Number of Spanning Trees) vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('ln(Number Spanning Trees)')
y_max = max([max(trees[0]['ln_ST']), max(trees[1]['ln_ST'])] )
x_max = max([max(trees[1]['Num_vertices']), max(trees[0]['Num_vertices'])])
plt.text(x_max * 0.75, y_max * 0, st[0], c = cl[0])
plt.text(x_max * 0.75, y_max * 0.1, st[1], c = cl[1])
plt.legend()
plt.savefig('t_bg_nodes_lnst.png')