import spanningtrees
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

# opening pickle files
# may need to change directory depending on file locations, idk

# lattice data
with open('tree_const_sq.pkl', 'rb') as f:
    tree_const_sq = pickle.load(f)
with open('num_nodes_sq.pkl', 'rb') as f:
    num_nodes_sq = pickle.load(f)
with open('tree_const_tri.pkl', 'rb') as f:
    tree_const_tri = pickle.load(f)
with open('num_nodes_tri.pkl', 'rb') as f:
    num_nodes_tri = pickle.load(f)

# real data
with open('tree_const_real.pkl', 'rb') as f:
    tree_const_real = pickle.load(f)
with open('num_nodes_real.pkl', 'rb') as f:
    num_nodes_real = pickle.load(f)
with open('log_trees_real.pkl', 'rb') as f:
    log_trees_real = pickle.load(f)

# real data is stored as a list of lists
# i want to have one long list instead
tree_const_real = tree_const_real[0] + tree_const_real[1] + tree_const_real[2]
num_nodes_real = num_nodes_real[0] + num_nodes_real[1] + num_nodes_real[2]

# plot
plt.scatter(num_nodes_sq, tree_const_sq, c=['b']*len(num_nodes_sq))
plt.scatter(num_nodes_tri, tree_const_tri, c=['g']*len(num_nodes_tri))
plt.scatter(num_nodes_real, tree_const_real, c=['r']*len(num_nodes_real))
plt.ylim(1.0,1.65)
plt.title('ST Constant vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('ST Constant')
plt.legend(['square lattice','triangle lattice', 'real data'])
plt.show()

# plot log of span trees v num of nodes
log_trees_sq = np.multiply(tree_const_sq,num_nodes_sq).tolist()
log_trees_tri = np.multiply(tree_const_tri,num_nodes_tri).tolist()
log_trees_real = np.multiply(tree_const_real,num_nodes_real).tolist()

num_nodes = [num_nodes_sq, num_nodes_tri, num_nodes_real]
log_trees = [log_trees_sq, log_trees_tri, log_trees_real]
q = ['square', 'triangular', 'real']
cl = ['b','g','r']
trend = []
line = []
st = [[],[],[]]
for p in [0, 1, 2]:
    trend = np.polyfit(num_nodes[p], log_trees[p], 1)
    line = np.poly1d(trend)
    plt.scatter(num_nodes[p], log_trees[p], c = [cl[p]]*len(num_nodes[p]), label = q[p])
    plt.plot(num_nodes[p], line(num_nodes[p]), 'k')
    # display eq of line to four digits
    st[p] = 'y = ' + str(trend[0])[0:4] + 'x + ' + str(trend[1])[0:4]
plt.title(' Log(Spanning Trees) vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('Log(Spanning Trees)')
y_max = max([max(log_trees[0]), max(log_trees[1]), max(log_trees[2])])
x_max = max([max(num_nodes[0]), max(num_nodes[1]), max(num_nodes[2])])
plt.text(x_max * 0.75, y_max * 0, st[0], c = cl[0])
plt.text(x_max * 0.75, y_max * 0.1, st[1], c = cl[1])
plt.text(x_max * 0.75, y_max * 0.2, st[2], c = cl[2])
plt.legend()
plt.show()

from spanningtrees import makeRandomLattice
from spanningtrees import ST_const

"""
# now we do random lattice calculations
tree_const_rand = [[],[],[],[]]
num_nodes_rand = [[],[],[],[]]
prob = [0.25, 0.5, 0.75, 1]
q = [0,1,2,3]
for length in range(2,51):
    for p in q:
        print('calculating', 2*length, 'by', 2*length, 'with probability', prob[p])
        g_rand = makeRandomLattice([2*length,2*length],prob[p])
        (ST,n) = ST_const(g_rand)
        tree_const_rand[p].append(ST)
        num_nodes_rand[p].append(n)

# plot st constant v num of nodes
plt.scatter(num_nodes_real, tree_const_real, c = 'm', label = 'real')

cl = ['b', 'g', 'r','c']
q = ['0.25', '0.5', '0.75', '1']
for p in [0,1,2,3]:
    plt.scatter(num_nodes_rand[p], tree_const_rand[p], c = [cl[p]]*len(num_nodes_rand[p]), label = q[p], alpha = 0.4)
plt.ylim(1.0,1.65)
plt.title('ST Constant vs Number of Nodes')
plt.xlabel('Number of Nodes')
plt.ylabel('ST Constant')
plt.legend()
plt.show()
"""


