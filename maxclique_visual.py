from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

def deleted_nodes(node_for_delete):

    for node_partner in adj_list[node_for_delete]:
        if G.has_edge(str(node_for_delete),str(node_partner)):
            G.remove_edge(str(node_for_delete),str(node_partner))

def draw_and_show():
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

def erase_colors():
    for i in adj_list.keys():
        if colors[int(i)] != "#006633":
            colors[int(i)] = "#C0C0C0"
    draw_and_show()

def visualization(vertex_name, color_of_vertex):
    if colors[int(vertex_name)] != color_of_vertex:
        colors[int(vertex_name)] = color_of_vertex

def elimination(node):
    #Store maximal cliques than contain members of N(node) U node.
    list_of_max_cliques = []
    L1_list,L2_list = bfs(node)
    cliques_of_N1 = find_maximal_cliques(L1_list,node)
    for item in cliques_of_N1:
        list_of_max_cliques.append(item)
    output_of_compute_func = compute_max_clique(cliques_of_N1,L2_list,node)
    for item in output_of_compute_func:
        list_of_max_cliques.append(item)
    print("Maximal cliques that contain members of N(" +str(node)+ ")U{" +str(node)+ "} : ")
    print(str(list_of_max_cliques))
    max_degree_in_cliques = max(len(set_in_list) for set_in_list in list_of_max_cliques)
    #Return the largest clique of N(node) U node.
    for set_max in list_of_max_cliques:
        if len(set_max) == max_degree_in_cliques:
            print("Largest clique of N("+ str(node) +")U{" + str(node) +"} is " +str(set_max))
            for item_of_set in set_max:
                #xaki -green.
                visualization(item_of_set,"#336600")
            draw_and_show()
            for item_of_set in set_max:
                visualization(item_of_set,"#C0C0C0")
            draw_and_show()
            break
    #Delete N(u)U{u} from the graph and update the degrees of the remaining vertices.
    for neighbor_node in adj_list[node]:
        deleted_nodes(neighbor_node)
        colors[int(neighbor_node)] = "#202020"
        adj_list.pop(neighbor_node)
    for neighbors in adj_list.values():
        for vertex in neighbors:
            if vertex not in adj_list.keys():
                neighbors.remove(vertex)
    delete_nodes = []
    for item in adj_list.keys():
        if len(adj_list[item])==0:
            colors[int(item)] = "#202020"
            delete_nodes.append(item)
    for item_for_delete in delete_nodes:
        adj_list.pop(item_for_delete)
    colors[int(node)] = "#202020"
    adj_list.pop(node)
    return set_max

def compute_max_clique(cliques,L2,input_node):

    set_L2 = set(L2)
    maximal_cliques = []
    for clique in cliques:
        #print("Clique " + str(clique))
        for item_in_clique in clique:
            visualization(item_in_clique,"#FFFF33")
        draw_and_show()
        for vertex in clique:
            if vertex != input_node:
                #print("Clique " + str(clique))
                #print("Vertex from clique: " +str(vertex))
                visualization(vertex,"#006633")
                draw_and_show()
                adj_list[vertex] = set(adj_list[vertex])
                #Compute set Ax = N(x) Ո N2(u).
                #print("N(" + str(vertex) + "): " + str(adj_list[vertex]))
                for elem in adj_list[vertex]:
                    visualization(elem,"#FF8000")
                draw_and_show()
                #print("N2(" +str(input_node) +"):" + str(set_L2))
                for elem in set_L2:
                    visualization(elem,"#663300")
                draw_and_show()
                set_Ax = set_L2.intersection(adj_list[vertex])
                for item_in_Ax in set_Ax:
                    visualization(item_in_Ax,"#990099")
                #Check if set_A(x) is empty.
                if set_Ax:
                    draw_and_show()
                    #print("Intersection: " +str(set_Ax))
                    for i in adj_list.keys():
                        visualization(i,"#C0C0C0")
                    visualization(vertex,"#006633")
                    draw_and_show()
                    #Compute all maximal cliques of G[Ax].
                    output_of_Ax = find_maximal_cliques(set_Ax,vertex)
                    maximal_cliques.append(output_of_Ax)
                else:
                    #print("Intersection is empty set.")
                    for i in adj_list.keys():
                        visualization(i,"#C0C0C0")
                    draw_and_show()
    return maximal_cliques

def find_maximal_cliques(list_L1,input_node):
    list_of_cliques = []
    P = list_L1
    #Algorithm Bron-Kerbosch listing all maximal cliques of P.
    BronKerbosch(P)
    for list in BronKerbosch(P):
        list.add(input_node)
        #print("A maximal clique is found." + str(list))
        for i in adj_list.keys():
            if str(i) in list:
                visualization(i,"#FF0000")
            else:
                visualization(i,"#C0C0C0")
        draw_and_show()
        for element_of_clique in list:
            if element_of_clique != input_node:
                visualization(element_of_clique,"#C0C0C0")
        visualization(input_node,"#006633")
        draw_and_show()
        list_of_cliques.append(list)
    for i in adj_list.keys():
        if i != input_node:
            visualization(i,"#C0C0C0")
    visualization(input_node,"#C0C0C0")
    draw_and_show()
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
        yield from BronKerbosch(
            P=P.intersection(adj_list[v]), R=R.union([v]), X=X.intersection(adj_list[v]))
        X.add(v)

def bfs(root):

    visualization(root,"#006633")
    draw_and_show()
    visited_nodes = {}
    level = {}
    #Add L1,L2.
    L1 = []
    L2 = []
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
                        L1.append(neighbor)
                        visualization(neighbor,"#FFFF33")
                    if level[neighbor] == 2:
                        L2.append(neighbor)
                        visualization(neighbor,"#FF8000")
                    queue.put(neighbor)
    if (not L1):
        print("L1 set is empty.")
        print("List of all maximal cliques " + str(list_of_all_max_cliques))
        print("Largest clique of graph is " +str(largest_clique))
        exit()
    if (not L2):
        print("L2 set is empty.")
        print("List of all maximal cliques " + str(list_of_all_max_cliques))
        print("Largest clique of graph is " +str(largest_clique))
        exit()

    print("L1 set" +str(L1))
    print("L2 set" +str(L2))
    draw_and_show()
    erase_colors()

    return L1,L2

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

    #Compute threshold.
    f_threshold = edges_num ** (1/3)

    #Visualize the graph with all nodes and edges.
    pos = nx.circular_layout(G)
    colors = nx.get_node_attributes(G,'color').values()
    colors = list(colors)
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

    return adjacency_list,nodes_num,f_threshold,pos,colors

###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")

#Create graph for visualization.
G = nx.Graph()
#Create the adjacency list.
adj_list,nodes_num,threshold,pos,colors = graph_file(inputFile)
#Find Δ(G)(maximum vertex degree in graph).
max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
print("Threshold: " +str(threshold))
print("Δ(G): " +str(max_degree))

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
            print("Node of degree Δ(G): " + str(v_vertex))
            result_clique = elimination(v_vertex)
            list_of_all_max_cliques.append(result_clique)
            print("Previous Δ(G) is " +str(max_degree))
            #Calculate maximum degree Δ(G) of the remaining graph.
            max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
            print("Δ(G) of the remaining graph is " +str(max_degree))
            #break from loop for and check loop while
            break
#print("List of all max cliques " + str(list_of_all_max_cliques))
temp_array=[]
for elem in adj_list.keys():
    temp_array.append(elem)
print("Remaining nodes in graph " +str(temp_array))
draw_and_show()
#For every vertex of the remaining graph enumerate all maximal cliques.
for vertex_v in adj_list.keys():

    print("Node " +str(vertex_v))
    L1_list,L2_list = bfs(vertex_v)
    #Enumerate all maximal cliques of the remaining graph containing vertex_v of the remaining graph.
    output_from_find_func = find_maximal_cliques(L1_list,vertex_v)
    print("Maximal cliques that contain {" +str(vertex_v)+ "} : " + str(output_from_find_func))
    largest_clique_of_output = max(len(set_of_output) for set_of_output in output_from_find_func)
    for set_of_output in output_from_find_func:
        #Check for eliminate duplicate sets in list_of_all_max_cliques.
        if (set_of_output not in list_of_all_max_cliques) and (len(set_of_output) == largest_clique_of_output):
            print("Largest clique is " +str(set_of_output))
            for item_output in set_of_output:
                visualization(item_output,"#336600")
            draw_and_show()
            for item_output in set_of_output:
                visualization(item_output,"#C0C0C0")
            draw_and_show()
            list_of_all_max_cliques.append(set_of_output)
    #Find the largest size of all cliques which hane been stored.
    size_of_largest = max(len(set_of_cliques) for set_of_cliques in list_of_all_max_cliques)
    #Note a largest clique of the original graph.If there are many cliques with the largest size then choose the first one of the list.
    for largest_clique in list_of_all_max_cliques:
        if len(largest_clique) == size_of_largest:
            break

print("List of all maximal cliques " + str(list_of_all_max_cliques))
print("Largest clique of graph is " +str(largest_clique))
for item in largest_clique:
    visualization(item,"#336600")
draw_and_show()

#Close file.
inputFile.close()
