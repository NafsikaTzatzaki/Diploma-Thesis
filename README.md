# Diploma-Thesis

The aim of this work is to present and implement algorithms for identifying problems and finding maximum clique problems related to diamond-free graphs. 
A graph is diamond-free if it does not contain a diamond as an induced subgraph. The application concerns simple, coherent, and undirected graphs. 
The core process is an algorithm that checks whether a particular node of the graph is part of an induced C4 or diamond using the search algorithm Βreadth-First Search. 
This process is part of a C4 or diamond induced subgraph recognition algorithm on the whole graph.A graph is (C4, diamond)-free if it contains neither C4 nor diamond 
as an induced subgraph. Finding a maximum clique in a (house, diamond)-free graph is also a problem and object of the work.The process of locating and enumerating 
all cliques, including the maximum cliques, helps to find the largest clique in a graph. Maximum clique is a clique with the maximum possible number of nodes. 
Additionally, for the recognition problem, another alternative approach to recognizing graph diamonds is presented.The algorithms are implemented using the Python 
programming language. Finally, with the use of the Python libraries NetworkX and Matplotlib we render visually and comprehensibly the steps of each algorithm to examine 
their correct implementation.


### recognition_3_1.py 

The algorithm recognizes whether a specific node in the graph belongs to an induced diamond subgraph. 
Specifically, the algorithm takes a graph and a node of the graph as input, 
checks whether the node is contained in an induced diamond or C4 subgraph of the input graph, and returns the result. 
Specifically, it returns True if the node belongs to an induced C4 or diamond subgraph, 
otherwise it returns False indicating that the node does not belong to an induced C4 or diamond subgraph.


### recognition_3_2.py 
The algorithm recognizes whether a graph is (C4, diamond)-free, meaning it checks if there is an induced diamond subgraph (as shown in Figure 1.1) or 
an induced C4 subgraph (as shown in Figure 1.2) in the entire graph.
The basic strategy being applied focuses on the degree of the nodes in the graph. When the maximum degree in a graph is sufficiently high, we identify a node with the maximum degree and remove it from the graph along with all of its neighboring nodes. Before we proceed with the process of eliminating the node and its neighbors, we check a series of cases from which we can identify that the node is part of a C4 or diamond-induced subgraph, and therefore our graph is not (C4,diamond)-free. Through these cases, we can identify whether the node or any of its neighboring nodes is part of a C4 or diamond subgraph and in case of detection, we extract the result for the graph. If after checking all cases, no condition that declares the detection of C4 or diamond is satisfied, we proceed with the process of eliminating the nodes from the graph, renewing the degrees of the remaining nodes in the graph.
The algorithm takes as input a graph and returns True if the graph is (diamond,C4)-free,otherwise it returns False.
