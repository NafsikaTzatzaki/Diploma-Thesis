# Input(graph_1.txt or graph_2.txt) : Output False.
# Input(graph_3.txt) : Output True.

from queue import Queue

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

def bfs(root):

    visited_nodes = {}
    level = {}
    parent = {}
    # Add L1,L2.
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
    return distance_L1,distance_L2,parent,level

def Case_1a(L1):
    #Case 1a: If l1 does not induce a disjoint union of cliques then return no.
    for node_in_L1 in L1:
        for neighbor_of_node in adj_list[node_in_L1]:
            if neighbor_of_node in L1:
                for neighbor_of_neigh in adj_list[neighbor_of_node]:
                    if neighbor_of_neigh != node_in_L1:
                        #If a P3 found then return False.
                        if (neighbor_of_neigh in L1) and (neighbor_of_neigh not in adj_list[node_in_L1]):
                            return False
    return True

def Case_1b(L1,L2):
    #Case 1b: If a vertex in l2 sees two or more vertices in l1 then return no.
    counter_two_vertices = 0
    for item_in_L2 in L2:
        counter_two_vertices = 0
        for item_in_L1 in L1:
            if counter_two_vertices < 2 :
                if item_in_L1 in adj_list[item_in_L2]:
                    counter_two_vertices += 1
            else:
                return False
    return True

def Case_1c(L1,L2):
    """Case 1c: For each vertex wεL1 do
                 if N(w)^L2 does not induce a disjoint union of cliques then return no."""
    for item_in_L1 in L1:
        #Find intersection of N(w)ՈL2.
        set_intersect = []
        for neighbor in adj_list[item_in_L1]:
            if neighbor in L2:
                set_intersect.append(neighbor)
        #Check if intersection of N(w)ՈL2 does not induce a disjoint union of cliques.
        for node_in_intersect in set_intersect:
            for neighbor_of_node in adj_list[node_in_intersect]:
                if neighbor_of_node in set_intersect:
                    for neighbor_of_neigh in adj_list[neighbor_of_node]:
                        if neighbor_of_neigh!=node_in_intersect:
                            #If a P3 found then return False.
                            if (neighbor_of_neigh in set_intersect) and (neighbor_of_neigh not in adj_list[node_in_intersect]):
                                return False
    return True

def Case_1d(L2,parent,level):
    """Case 1d : For each edge xy with xεL2 and yεL2 do
                   Let x' = parent(x) and  y' = parent(y)
                   if x'sees y' then return no. """
    for item_in_L2 in L2:
        for neighbor in adj_list[item_in_L2]:
            if level[neighbor]==2:
                if parent[item_in_L2] in adj_list[parent[neighbor]]:
                    return False
    return True

def Case_1e(L2,parent,level):
    #Case 1e: If xεL2 sees aεL2 and bεL2 such that parent(a)=parent(b),but parent(x)!= parent(b) then return no.
    for item_in_L2 in L2:
        a_vertex = None
        b_vertex = None
        for neighbor in adj_list[item_in_L2]:
            if neighbor in L2:
                if a_vertex == None:
                    a_vertex = neighbor
                else:
                    b_vertex = neighbor
                    if parent[a_vertex]==parent[b_vertex] and parent[item_in_L2]!=parent[a_vertex]:
                        return False
    return True

def Case_1f(L2,parent,level):
    #Case 1f: If xεL2 sees aεL2 and bεL2 such that parent(a)=parent(b) then return no.
    for item_in_L2 in L2:
        a_vertex = None
        b_vertex = None
        for neighbor in adj_list[item_in_L2]:
            #if neighbor in L2:
            if level[neighbor]==2 :
                if a_vertex == None:
                    a_vertex = neighbor
                else:
                    b_vertex = neighbor
                    if parent[a_vertex]==parent[b_vertex]:
                        return False
    return True

def elimination(node):
    #Perform breadth-first search from v until all vertices at distance 3 from v are marked.
    L1_list,L2_list,parent_list,level_list = bfs(node)

    result_from_case = Case_1a(L1_list)
    #If result_from_case is True then continue to check next case else return False.
    if result_from_case:
        result_from_case = Case_1b(L1_list,L2_list)
    if result_from_case:
        result_from_case = Case_1c(L1_list,L2_list)
    if result_from_case:
        result_from_case = Case_1d(L2_list,parent_list,level_list)
    if result_from_case:
        result_from_case = Case_1e(L2_list,parent_list,level_list)
    if result_from_case:
        result_from_case = Case_1f(L2_list,parent_list,level_list)

    #If the result of last case is True then delete N(u)v{u} from the graph and update the degrees of the remaining vertices.
    if result_from_case:
        for neighbor_node in adj_list[node]:
            adj_list.pop(neighbor_node)
        for neighbors in adj_list.values():
            for vertex in neighbors:
                if vertex not in adj_list.keys():
                    neighbors.remove(vertex)
                    #G.remove_node(int(vertex))
        adj_list.pop(node)
    return result_from_case

def OmD_alg(root):
    visited_nodes = {}
    level = {}
    BFS_output = []
    queue = Queue()

    for node in adj_list.keys():
        visited_nodes[node] = False
        level[node] = -1 #inf.
    #root of breadth-first search.
    visited_nodes[root] = True
    level[root] = 0
    queue.put(root)
    current_node = None
    level[current_node]=0

    while not queue.empty():
        #Store 2 common neighbors between a non-neighbor of root and the root.
        neighbors_of_root = []
        current_node = queue.get()

        #Mark all vertices at distance two from root.
        if level[current_node] < 3 :
            BFS_output.append(current_node)
            for neighbor in adj_list[current_node]:
                if not visited_nodes[neighbor] :
                    visited_nodes[neighbor] = True
                    level[neighbor] = level[current_node] + 1
                    queue.put(neighbor)
                #If a non-neighbor of root(current_node) share a neighbor with root,append neighbor in neighbors_of_root list.
                elif level[current_node]== 2 and level[neighbor]== 1 :
                    neighbors_of_root.append(neighbor)
            #If neighbors_of_root list store at least 2 nodes,then v_vertex is in an induced diamond or C4.
            if len(neighbors_of_root)>=2:
                print("C4 or diamond is found.")
                return False
    return True

###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")

adj_list,threshold = graph_file(inputFile)

#Find Δ(G)(maximum vertex degree in graph).
max_degree = max(len(adj_list[vertex]) for vertex in adj_list)

result = True
#Loop while Δ(G) is above the threshold f.
while max_degree > threshold:
    for key,value in list(adj_list.items()):
        #Find a vertex v of degree Δ(G).
        if len(value) == max_degree:
            v_vertex = key
            # Function 'elimination' check all possible cases so as to find C4 or diamond in graph.
            # If a case return False then print False and exit() because graph contains C4 or diamond.
            # If all cases return True then Function 'elimination' eliminate v and N(v)(neighbors of v) from consideration.
            result = elimination(v_vertex)
            if result:
                max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
                break
            else:
                print("result " + str(result))
                exit()

#If Δ(G) <= threshold f and result_from_case is True then run OmD algorithm for each node for the remaining graph.
for node in adj_list:
    result = OmD_alg(node)
    #If the result from OmD algorithm is True then continue to next node else break and print False.
    if not result:
        break

print("result " + str(result))
inputFile.close()
