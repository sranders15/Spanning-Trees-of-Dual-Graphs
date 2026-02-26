# Splittability of Dual Graphs

The code in this repository is based heavily on https://github.com/brookecarofeinberg/SamplingBalancedForests, though a small bug (that had little influence on the conclusions) has been fixed. 


`splitability_functions.py`: Contains functions used to calculate how likely it is that a random spanning tree of a graph can be split into ewaul-sized pieces, including Wilson's Algorithm for generating random spanning trees and a Graph Partition function that checks a tree for splittability. 

`Splittability_Calculator.py`: This code takes as input a level of geography and a state, and generates random spanning trees until 178 splittable random spanning trees have been found.  Writes results to `cnty_results.csv`, `t_results.csv`, or `bg_results.csv` as appropriate. 

`cnty_results.csv`: The results of our experiments on county graphs, including the number of trials needed to achieve 178 successes (where a success is generating a random spanning tree that's splittable).

`t_results.csv`: The results of our experiments on tract graphs, including the number of trials needed to achieve 178 successes 

`bg_results.csv`: The results of our experiments on block group graphs, including the number of trials needed to achieve 178 successes 

`regression_visualization.ipynb`: This code visualizes the relationship between the (log of the) splittability probability and the (log of the) number of vertices of a graph and performs regression to assess this relationship. 

`fig/`: A subfolder storing the images generated in `regression_visualization.ipynb`