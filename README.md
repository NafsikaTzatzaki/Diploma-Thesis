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

The algorithm recognizes whether a graph is (C4, diamond)-free, meaning it checks if there is an induced diamond subgraph or 
an induced C4 subgraph in the entire graph.
The basic strategy being applied focuses on the degree of the nodes in the graph. When the maximum degree in a graph is sufficiently high, we identify a node with the maximum degree and remove it from the graph along with all of its neighboring nodes. Before we proceed with the process of eliminating the node and its neighbors, we check a series of cases from which we can identify that the node is part of a C4 or diamond-induced subgraph, and therefore our graph is not (C4,diamond)-free. Through these cases, we can identify whether the node or any of its neighboring nodes is part of a C4 or diamond subgraph and in case of detection, we extract the result for the graph. If after checking all cases, no condition that declares the detection of C4 or diamond is satisfied, we proceed with the process of eliminating the nodes from the graph, renewing the degrees of the remaining nodes in the graph.
The algorithm takes as input a graph and returns True if the graph is (diamond,C4)-free,otherwise it returns False.


### enumerate_max_cliques.py

The algorithm takes as input a graph that is (house, diamond)-free and a node u in the graph. 
It computes the set of maximum cliques that intersect the set N(u) U {u}. More specifically, the algorithm identifies all cliques in the graph that either contain the input node u or contain at least one neighbor of the input node.

### maxclique.py

The algorithm takes as input a (house, diamond)-free graph and computes the largest clique in the graph.
The algorithm is a composition of the previous algorithms that we have analyzed, as all of them together contribute to solving the problem of finding the maximum clique.
To implement it, we use the basic strategy of recognition_3_2.py that focuses on the degree of the nodes in the graph.
As long as the highest degree of a node in the graph exceeds the threshold, we execute the enumerate_maximal_cliques.py algorithm to identify the set of maximum cliques.
At the end, from all the maximal cliques we have stored for the respective subsets of nodes in the graph, we identify the largest clique which is the goal of the algorithm.

### recognition_of_diamonds.py

The algorithm recognizes whether a graph is diamond-free. In this implementation, the process of checking for a diamond within the graph is divided into four phases. Before executing the phases, the algorithm separates the nodes into low-degree L and high-degree H. This separation is based on a threshold D.
The process of the first phase checks if there is a diamond as an induced subgraph with a degree-3 node in the subgraph belonging to the low-degree L nodes. In the second phase, it is checked if there is a diamond as an induced subgraph with a degree-2 node belonging to the low-degree L nodes. If no diamond has been found in the previous phases, we move on to the third phase. In the third phase, we remove all low-degree nodes from the graph and update the adjacency lists of the remaining nodes. In the fourth phase, we perform the process from the beginning by checking if there is a diamond in the remaining graph. The algorithm returns True if G is diamond-free, otherwise, it returns False.

***The files (_visual) also contain the code related to the visualization of each algorithm.
