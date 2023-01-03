from queue import Queue

def find_maximal_cliques(list_L1,input_node):
    list_of_cliques = []
    P = list_L1
    #Algorithm Bron-Kerbosch listing all maximal cliques of set P.
    BronKerbosch(P)
    for list in BronKerbosch(P):
        list.add(input_node)
        print("A maximal clique is found: " +str(list))
        list_of_cliques.append(list)
    return list_of_cliques

def BronKerbosch(P,R=None,X=None):
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from BronKerbosch(
            P=P.intersection(adj_list[v]), R=R.union([v]), X=X.intersection(adj_list[v]))
        X.add(v)

def compute_max_cliques(cliques):
    set_L2 = set(L2)
    maximal_cliques = []
    for clique in cliques:
        for vertex in clique:
            if vertex !=input_vertex:
                adj_list[vertex] = set(adj_list[vertex])
                #Compute set Ax = N(vertex) Λ N2(input_node).
                set_Ax = set_L2.intersection(adj_list[vertex])
                #Check if set_A(x) is empty.
                if set_Ax:
                    #Compute all maximal cliques of G[Ax].
                    output_of_Ax = find_maximal_cliques(set_Ax,vertex)
                    for set_of_Ax in output_of_Ax:
                        if set_of_Ax not in maximal_cliques:
                            maximal_cliques.append(set_of_Ax)
    return maximal_cliques

def bfs(root):

    visited_nodes = {}
    level = {}
    parent = {}
    distance_L1 = []
    distance_L2 = []
    BFS_output = []
    queue = Queue()

    for node in adj_list.keys():
        visited_nodes[node] = False
        parent[node]= None
        level[node] = -1 #inf.
    #root.
    visited_nodes[root] = True
    level[root] = 0
    queue.put(root)
    current_node = None
    level[current_node]=0

    while not queue.empty():
        neighbors_of_root = []
        current_node = queue.get()
        #Mark all vertices at distance three from root.
        if level[current_node] < 3 :
            BFS_output.append(current_node)
            for neighbor in adj_list[current_node]:
                if not visited_nodes[neighbor] :
                    visited_nodes[neighbor] = True
                    parent[neighbor] = current_node
                    level[neighbor] = level[current_node] + 1
                    if level[neighbor] == 1:
                        distance_L1.append(neighbor)
                    if level[neighbor] == 2:
                        distance_L2.append(neighbor)
                    queue.put(neighbor)
    return distance_L1,distance_L2

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())
    node_input = input("Choose node from 0 to " + str(nodes_num-1)+ ": ")

    #Check if edges >= (nodes-1).
    if edges_num < (nodes_num-1):
        print("Statement: edges >= (nodes-1) is violated.")
        exit()

    adjacency_list = {}
    for readline in file :
        edge = readline.strip()
        nodes_from_edge = edge.split("-")
        node1 = nodes_from_edge[0]
        node2 = nodes_from_edge[1]

        #Check if edge's nodes have the same name.
        if node1 == node2:
            print("Error: edge's nodes have the same label.")
            exit()
        #Check if the labels of nodes are out of range.
        if (int(node1) >= nodes_num or int(node1)< 0) or (int(node2) >= nodes_num or int(node2)< 0):
            print("Error: Label out of range is found.")
            exit()
        for node in nodes_from_edge:
            #Check if each node of the edge exists in adj_list.If one of them doesn't exist,add node to the dictionary by using the update() method.
            if node not in adjacency_list:
                adjacency_list.update({node:[]})
        #Check for duplicate edges.
        if (node1 in adjacency_list[node2]) and (node2 not in adjacency_list[node1]):
            edges_num = edges_num -1
        else:
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)
    #Check if edges is at least nodes-1.
    if edges_num < (nodes_num-1):
        print("Statement edges >= (nodes-1) is violated.")
        exit()

    return adjacency_list,node_input

###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Create the adjacency list.
adj_list,input_vertex = graph_file(inputFile)
#Breadth first search algorithm starting from input_vertex.
L1,L2 = bfs(input_vertex)

#Find maximal cliques of G[N(input_vertex)].
cliques_of_N1 = find_maximal_cliques(L1,input_vertex)
#Output maximal cliques of G[N(input_vertex)] U {input_vertex}.
print(" Cliques of N1 " +str(cliques_of_N1))
#Compute maximal cliques of G[N(input_vertex) Ո N2(input_vertex)].
set_of_max_cliques = compute_max_cliques(cliques_of_N1)
print("Set of max cliques " +str(set_of_max_cliques))
for clique in cliques_of_N1:
    set_of_max_cliques.append(clique)
print("Maximal cliques " + str(set_of_max_cliques))

#close file.
inputFile.close()
