from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

def draw_and_show():
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

def visualization(vertex_name, color_of_vertex):
    if colors[int(vertex_name)] != color_of_vertex:
        colors[int(vertex_name)] = color_of_vertex

def find_maximal_cliques(list_L1,input_node):
    list_of_cliques = []
    P = list_L1
    #Algorithm Bron-Kerbosch listing all maximal cliques of set P.
    BronKerbosch(P)
    for list in BronKerbosch(P):
        list.add(input_node)
        #print("Maximal clique is found " + str(list))
        for element_of_clique in list:
            visualization(element_of_clique,"#FF0000")
        draw_and_show()
        for element_of_clique in list:
            if element_of_clique != input_node:
                visualization(element_of_clique,"#C0C0C0")
        visualization(input_node,"#006633")
        draw_and_show()
        list_of_cliques.append(list)
    for i in range(nodes_num):
        if i != input_node:
            visualization(i,"#C0C0C0")
    visualization(input_node,"#C0C0C0")
    draw_and_show()
    print("Maximal cliques of set N(" +str(input_vertex)+ ")UL2 :" + str(list_of_cliques))
    return list_of_cliques

def BronKerbosch(P,R=None,X=None):
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        visualization(v,"#000066")
        draw_and_show()
        #print("Node " +str(v))
        yield from BronKerbosch(
            P=P.intersection(adj_list[v]), R=R.union([v]), X=X.intersection(adj_list[v]))
        visualization(v,"#C0C0C0")
        X.add(v)

def compute_max_cliques(cliques):
    set_L2 = set(L2)
    maximal_cliques = []
    for clique in cliques:
        for item_in_clique in clique:
            visualization(item_in_clique,"#FFFF33")
        draw_and_show()
        for vertex in clique:
            if vertex !=input_vertex:
                visualization(vertex,"#FF8888")
                draw_and_show()
                adj_list[vertex] = set(adj_list[vertex])
                #Compute set Ax = N(vertex) Ո N2(input_node).
                set_Ax = set_L2.intersection(adj_list[vertex])
                for item_in_Ax in set_Ax:
                    visualization(item_in_Ax,"#990099")
                #Check if set_A(x) is empty.
                if set_Ax:
                    draw_and_show()
                    #print("N(" +str(input_node)+ ") Ո (N2(" +str())
                    print("Intersection of set L2 and N("+ str(vertex)+ ") is set " +str(set_Ax))
                    for i in range(nodes_num):
                        if colors[int(i)] != "#006633" and colors[int(i)] != "#990099":
                            visualization(i,"#C0C0C0")
                    draw_and_show()
                    #green.
                    visualization(vertex,"#006633")
                    draw_and_show()
                    #Compute all maximal cliques of G[Ax].
                    output_of_Ax = find_maximal_cliques(set_Ax,vertex)
                    for set_of_Ax in output_of_Ax:
                        if set_of_Ax not in maximal_cliques:
                            maximal_cliques.append(set_of_Ax)
                else:
                    for i in range(nodes_num):
                        visualization(i,"#C0C0C0")
                    draw_and_show()
    return maximal_cliques

def bfs(root):
    #green.
    visualization(root,"#006633")
    visited_nodes = {}
    level = {}
    #Add L1,L2.
    distance_L1 = []
    distance_L2 = []
    BFS_output = []
    queue = Queue()

    for node in adj_list.keys():
        visited_nodes[node] = False
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
                    level[neighbor] = level[current_node] + 1
                    if level[neighbor] == 1:
                        distance_L1.append(neighbor)
                        visualization(neighbor,"#FFFF33")
                    if level[neighbor] == 2:
                        distance_L2.append(neighbor)
                        visualization(neighbor,"#FF8000")
                    queue.put(neighbor)
    if (not distance_L1):
        print("Set L1 is empty. Graph is (C4,diamond)-free.")
        exit()
    if (not distance_L2):
        print("Set L2 is empty. Graph is (C4,diamond)-free.")
        exit()
    print("L1 set " +str(distance_L1))
    print("L2 set " +str(distance_L2))
    draw_and_show()
    for i in range(nodes_num):
        if colors[int(i)] != "#006633":
            colors[int(i)] = "#C0C0C0"
    draw_and_show()
    return distance_L1,distance_L2

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())
    node_input = input("Choose node from 0 to " + str(nodes_num-1)+ ": ")

    #Store the graph as a dictionary.
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
        #Add all nodes in the graph.
        for i in range(nodes_num):
            G.add_node(str(i),color = "#C0C0C0")

        #Check for duplicate edges.
        if (node1 in adjacency_list[node2]) and (node2 not in adjacency_list[node1]):
            edges_num = edges_num -1
        else:
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)
            G.add_edge(node1,node2)

    #Check if edges is at least nodes-1.
    if edges_num < (nodes_num-1):
        print("Statement edges >= (nodes-1) is violated.")
        exit()

    #Visualize the graph with all nodes and edges.
    pos = nx.circular_layout(G)
    colors = nx.get_node_attributes(G,'color').values()
    colors = list(colors)
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

    return adjacency_list,nodes_num,node_input,pos,colors

###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Create graph for visualization.
G = nx.Graph()
#Create the adjacency list.
adj_list,nodes_num,input_vertex,pos,colors = graph_file(inputFile)
#Breadth first search algorithm starting from input_vertex.
L1,L2 = bfs(input_vertex)

#Find maximal cliques of G[N(input_vertex)].
cliques_of_N1 = find_maximal_cliques(L1,input_vertex)
#Output maximal cliques of G[N(input_vertex)] U {input_vertex}.

#Compute maximal cliques of G[N(input_vertex) Ո N2(input_vertex)].
set_of_max_cliques = compute_max_cliques(cliques_of_N1)
#print("Set of max cliques " +str(set_of_max_cliques))
for clique in cliques_of_N1:
    set_of_max_cliques.append(clique)
visualization(input_vertex,"#006633")
for elem in L1:
    visualization(elem,"#009900")
print("The set of maximal cliques that intersect N(" +str(input_vertex)+ ")U{" +str(input_vertex)+ "} :")
print(set_of_max_cliques)
draw_and_show()

#close file.
inputFile.close()
