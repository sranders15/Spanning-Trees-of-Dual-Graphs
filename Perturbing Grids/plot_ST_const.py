import spanningtrees
import pickle
import os
import matplotlib.pyplot as plt

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
