from queue import Queue

def elimination(node):
    #Store maximal cliques than contain members of union(N(node),node).
    list_of_max_cliques = []
    #Breadth first search algorithm starting from node.
    L1_list,L2_list,level_list = bfs(node)
    #Find all maximal cliques of L1 list.
    cliques_of_N1 = find_maximal_cliques(L1_list,node)
    for item in cliques_of_N1:
        list_of_max_cliques.append(item)
    output_of_compute_func = compute_max_clique(cliques_of_N1,L2_list,node)
    for item in output_of_compute_func:
        list_of_max_cliques.append(item)
    max_degree_in_cliques = max(len(set_in_list) for set_in_list in list_of_max_cliques)
    #Return the largest clique of N(node) U node.
    for set_max in list_of_max_cliques:
        if len(set_max) == max_degree_in_cliques:
            break
    for neighbor_node in adj_list[node]:
        adj_list.pop(neighbor_node)
    for neighbors in adj_list.values():
        for vertex in neighbors:
            if vertex not in adj_list.keys():
                neighbors.remove(vertex)
    adj_list.pop(node)
    return set_max

def compute_max_clique(cliques,L2,input_node):

    set_L2 = set(L2)
    maximal_cliques = []
    for clique in cliques:
        for vertex in clique:
            if vertex != input_node:
                adj_list[vertex] = set(adj_list[vertex])
                #Compute set Ax = N(x) Λ N2(u).
                set_Ax = set_L2.intersection(adj_list[vertex])
                #Check if set_A(x) is empty.
                if set_Ax:
                    #Compute all maximal cliques of G[Ax].
                    output_of_Ax = find_maximal_cliques(set_Ax,vertex)
                    maximal_cliques.append(output_of_Ax)
    return maximal_cliques

def find_maximal_cliques(list_L1,input_node):
    list_of_cliques = []
    P = list_L1
    #Algorithm Bron-Kerbosch listing all maximal cliques of set P.
    BronKerbosch(P)
    for list in BronKerbosch(P):
        list.add(input_node)
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

def bfs(root):

    visited_nodes = {}
    level = {}
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
        #Mark all vertices at distance two from root.
        if level[current_node] < 3 :
            BFS_output.append(current_node)
            for neighbor in adj_list[current_node]:
                if not visited_nodes[neighbor] :
                    visited_nodes[neighbor] = True
                    level[neighbor] = level[current_node] + 1
                    if level[neighbor] == 1:
                        distance_L1.append(neighbor)
                    if level[neighbor] == 2:
                        distance_L2.append(neighbor)
                    queue.put(neighbor)
    return distance_L1,distance_L2,level

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())

    adjacency_list = {}
    for readline in file :
        edge = readline.strip()
        nodes_from_edge = edge.split("-")
        node1 = nodes_from_edge[0]
        node2 = nodes_from_edge[1]

        #Check if edge's nodes have the same label.
        if node1 == node2:
            print("Error: edge's nodes have the same label.")
            exit()
        #check if the labels of nodes are out of range.
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

    #Compute threshold.
    f_threshold = edges_num ** (1/3)

    return adjacency_list,f_threshold


###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Create the adjacency list.
adj_list,threshold = graph_file(inputFile)

#Find Δ(G)(maximum vertex degree in graph).
max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
result = True
#Store each largest clique of each set that contains N(v_vertex)U{v_vertex}.
list_of_all_max_cliques = []
#Loop while Δ(G) is above threshold f.
while max_degree > threshold:
    for key,value in list(adj_list.items()):
        #Find a vertex v of degree Δ(G).
        if len(value) == max_degree:
            v_vertex = key
            #Find the largest clique of that contain members of N(v_vertex)U{v_vertex}.
            result_clique = elimination(v_vertex)
            list_of_all_max_cliques.append(result_clique)
            #Calculate maximum degree Δ(G) of the remaining graph.
            max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
            #break from loop for and check loop while
            break

#For every vertex of the remaining graph enumerate all maximal cliques.
for vertex_v in adj_list:
    L1_list,L2_list,level_list = bfs(vertex_v)
    #Enumerate all maximal cliques of the remaining graph containing vertex_v of the remaining graph.
    output_from_find_func = find_maximal_cliques(L1_list,vertex_v)
    for set_of_output in output_from_find_func:
        #Check to eliminate duplicate sets in list_of_all_max_cliques.
        if set_of_output not in list_of_all_max_cliques:
            list_of_all_max_cliques.append(set_of_output)
    #Find the largest size of all cliques which have been stored.
    size_of_largest = max(len(set_of_cliques) for set_of_cliques in list_of_all_max_cliques)
    #Note a largest clique of the original graph.If there are many cliques with the largest size then choose the first one of the list.
    for largest_clique in list_of_all_max_cliques:
        if len(largest_clique) == size_of_largest:
            break

print("Largest clique " +str(largest_clique))

#Close file.
inputFile.close()
