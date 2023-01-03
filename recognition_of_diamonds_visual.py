from queue import Queue
from numpy.linalg import matrix_power
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

def draw_and_show():
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

def visualization(vertex_name, color_of_vertex):
    colors[int(vertex_name)] = color_of_vertex

def deleted_nodes(node_for_delete):

    for node_partner in adj_list[node_for_delete]:
        if G.has_edge(str(node_for_delete),str(node_partner)):
            G.remove_edge(str(node_for_delete),str(node_partner))

def bfs(root,secondary_element,component):
    visited_nodes = []
    BFS_output = []
    queue = Queue()
    #root of breadth-first search.
    queue.put(root)
    level=0
    compoment_without_root= component.copy()
    compoment_without_root.remove(root)

    while not queue.empty():
        current_node = queue.get()
        #Mark all vertices at distance two from root.
        BFS_output.append(current_node)
        level += 1
        for node_from_component in compoment_without_root:
            if adjacency_matrix[current_node][node_from_component] and (node_from_component not in visited_nodes):
                visited_nodes.append(node_from_component)
                queue.put(node_from_component)
                if level==2:
                    if node_from_component == secondary_element:
                        BFS_output.append(node_from_component)
                        return True,BFS_output
                    else:
                        print("Not Path")
                        return False,BFS_output

def function_phase_2(adjacency_matrix_2,vertex_x,stored_cliques):
    print("Phase 2")
    #Calculate adjacency_matrix x adjacency_matrix.
    for clique in stored_cliques:
        size_of_clique = len(clique)
        if len(clique)==1:
            print("Clique " +str(clique)+ " is size 1.")
        else:
            passed_nodes =[]
            for vertex_1 in clique:
                for vertex_2 in clique:
                    if (vertex_1 != vertex_2) and (vertex_2 not in passed_nodes):
                        print("Clique: " +str(clique))
                        print("(A^2)x,y: " +str(adjacency_matrix_2[vertex_1][vertex_2]))
                        print("|clique|: " +str(size_of_clique))
                        if adjacency_matrix_2[vertex_1][vertex_2] > (size_of_clique - 1):

                            #Producing a diamond.
                            for item in range(num_of_nodes):
                                if item != vertex_x:
                                    if adjacency_matrix[vertex_1][item] and adjacency_matrix[vertex_2][item] and not adjacency_matrix[vertex_x][item] :
                                        print("(A^2)x,y > |clique|-1.")
                                        print("Vertices " + str(vertex_x) + ", " + str(vertex_1) + ", " + str(vertex_2) + " have a common neighbor outside of N[vertex_low_degree] vertex " + str(item))
                                        print("Vertices " + str(vertex_x) + ", " + str(vertex_1) + ", " + str(vertex_2) + ", " + str(item) + " produce a diamond.")
                                        visualization(vertex_x,"#FF0000")
                                        visualization(vertex_1,"#FF0000")
                                        visualization(vertex_2,"#FF0000")
                                        visualization(item,"#FF0000")
                                        draw_and_show()
                                        exit()
                            #print("Elements have common neighbor outside of N[vertex_low_degree]. A diamond is found")
                        else:
                            print("(A^2)x,y <= |clique|-1.")
                passed_nodes.append(vertex_1)
def check_for_clique(vertex,component,array_of_cliques):
    Flag_for_clique = True
    for element_1 in component:
        for element_2 in component:
            if element_1 !=element_2 :
                #if element_1 and element_2 from set of component are not neighbors.
                if not adjacency_matrix[element_1][element_2]:
                    Flag_for_clique = False
                    result_from_BFS,BFS_output = bfs(element_1,element_2,component)
                    #if result from Breadth First Search is True then a P(3) is found.
                    if result_from_BFS:
                        print("Component is not clique. P3 is found " + str(BFS_output))
                        BFS_output.append(vertex)
                        print("Graph has an induced diamond " +str(BFS_output))
                        for elem in BFS_output:
                            visualization(elem,"#FF0000")
                        draw_and_show()
                        for elem in BFS_output:
                            visualization(elem,"#C0C0C0")
                        draw_and_show()
                        exit()
    #Ιf flag is True then compoment is a clique and add it in a list.
    if Flag_for_clique:
        array_of_cliques.append(component)
    return array_of_cliques

def find_vertex_degree():
    #Store nodes of low degree in a list.
    nodes_low_degree =[]
    #Calculate the degree of each vertex of the graph.
    for vertex in range(num_of_nodes):
        degree_of_vertex = 0
        for neighbor_of_vertex in range(num_of_nodes):
            if adjacency_matrix[vertex][neighbor_of_vertex] == 1:
                degree_of_vertex += 1
        #Ιf the degree is at the most as the upper limit of low degree vertices.
        if degree_of_vertex > 0 and degree_of_vertex < low_degree:
            nodes_low_degree.append(vertex)
    return nodes_low_degree

def search_diamond(adjacency_matrix):
    for vertex in nodes_low_degree:
        #Store the neighbors of vertex in a list.
        neighbors_array  = []
        stored_cliques = []
        #Find the neighbors of vertex.
        for neigh in range(num_of_nodes):
            if adjacency_matrix[vertex][neigh]==1:
                neighbors_array.append(neigh)
        print("For vertex of low degree " +str(vertex)+ " compute the components of set G[N(x)]=" +str(neighbors_array))
        visualization(vertex,"#006633")
        for elem_neighbor in neighbors_array:
            visualization(elem_neighbor,"#FFFF33")
        draw_and_show()
        for elem_neighbor in neighbors_array:
            visualization(elem_neighbor,"#C0C0C0")
        #Compute the components of the neighborhood of vertex.
        while neighbors_array:
            #Set to keep track of visited nodes of graph.
            visited_list = set()
            #Function dfs(Depth First Search) calculates and returns a component.
            component = dfs(visited_list,neighbors_array[0],neighbors_array[0],neighbors_array)
            #Remove the nodes of the component so as to avoid duplicate compoments.
            for item in component:
                neighbors_array.remove(item)
                visualization(item,"#FF8000")
            print("Component: " + str(component))
            draw_and_show()
            for item in component:
                visualization(item,"#C0C0C0")
            #Function check_for_clique checks if the component is a clique.
            stored_cliques = check_for_clique(vertex,component,stored_cliques)
        print("Cliques of set G[N(x)] : " +str(stored_cliques))
        #Function function_phase_2 for checking Phase 2 of the algorithm if we have cliques in neighborhood of vertex.
        adjacency_matrix_2 = np.zeros((num_of_nodes,num_of_nodes))
        for i in range(num_of_nodes):
            for j in range(num_of_nodes):
                for k in range(num_of_nodes):
                    adjacency_matrix_2[i][j] += adjacency_matrix[i][k] * adjacency_matrix[k][j]
        if stored_cliques:
            print("Stored cliques "+str(stored_cliques))
            function_phase_2(adjacency_matrix_2,vertex,stored_cliques)
        visualization(vertex,"#C0C0C0")
    #Remove all nodes of low degree from the graph.
    for neighbor_of_low_vertex in range(num_of_nodes):
        for low_degree_vertex in nodes_low_degree:
            #deleted_nodes(low_degree_vertex)
            colors[int(low_degree_vertex)] = "#202020"
            adjacency_matrix[low_degree_vertex][neighbor_of_low_vertex] = None
            adjacency_matrix[neighbor_of_low_vertex][low_degree_vertex] = None
            if G.has_edge(str(low_degree_vertex),str(neighbor_of_low_vertex)):
                G.remove_edge(str(low_degree_vertex),str(neighbor_of_low_vertex))
    draw_and_show()
    return adjacency_matrix

def dfs(visited,vertex_of_degree_3,node,neighbors_array):

    #Check if node is visited.
    if node not in visited:
        #Add node to the visited list.
        visited.add(node)
        for neighbor in range(num_of_nodes):
            #Check for item which is neighbor of node and belongs to neighborhood of the vertex.
            if adjacency_matrix[node][neighbor] and (neighbor in neighbors_array):
                #Call dfs for the neighbor of node.
                result = dfs(visited,vertex_of_degree_3,neighbor,neighbors_array)
    #return the component.
    return visited

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())

    #Calculate the upper limit of low degree vertices.
    max_low_degrees = math.sqrt(edges_num)
    #Initialize adjacency matrix.
    adj_matrix = np.zeros([nodes_num,nodes_num])
    #create the adjacency matrix.

    #Add all nodes in the graph.
    for i in range(nodes_num):
        #grey soft.
        G.add_node(str(i),color = "#C0C0C0")

    for readline in file :
        edge = readline.strip()
        nodes_from_edge = edge.split("-")
        node1 = int(nodes_from_edge[0])
        node2 = int(nodes_from_edge[1])

        #Check if edge's nodes have the same label.
        if node1 == node2:
            print("Error: edge's nodes have the same label.")
            exit()
        #check if the labels of nodes are out of range.
        if (node1 >= nodes_num or node1< 0) or (node2 >= nodes_num or node2< 0):
            print("Error: Label out of range is found.")
            exit()

        #Check for duplicate edges.
        if (adj_matrix[node1][node2] == 1) and (adj_matrix[node2][node1] == 1):
            edges_num = edges_num -1
        else:
            adj_matrix[node1][node2] = 1
            adj_matrix[node2][node1] = 1
            G.add_edge(str(node1),str(node2))

    #Check if edges >= (nodes-1).
    #Check if edges is at least nodes-1.
    if edges_num < (nodes_num-1):
        print("Statement: edges >= (nodes-1) is violated.")
        exit()
    #Visualize the graph with all nodes and edges.
    pos = nx.circular_layout(G)
    colors = nx.get_node_attributes(G,'color').values()
    colors = list(colors)
    nx.draw(G,pos,with_labels = 1, node_color=colors)
    plt.show()

    return adj_matrix,nodes_num,max_low_degrees,pos,colors

###-----------MAIN-----------###

#Variable file name: entered by user at runtime.
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Create graph for visualization.
G = nx.Graph()
#Check for unacceptable input node and graph's information and then create the adjacency list.
adjacency_matrix,num_of_nodes,low_degree,pos,colors = graph_file(inputFile)

#Store all cliques of the neighborhoods of low degree vertices.
stored_cliques = []
#Store low degree vertices in a list .
nodes_low_degree = find_vertex_degree()
print("Threshold: " +str(low_degree))
print("Vertices of low degree: " +str(nodes_low_degree))
for elem in nodes_low_degree:
    visualization(elem,"#FF8888")
draw_and_show()
for elem in nodes_low_degree:
    visualization(elem,"#C0C0C0")
draw_and_show()
#Do the procedure as long as there are nodes in the graph.
#flag_for_array = True
while nodes_low_degree:
    vertex_label = 0
    #Function than checks if there is a diamond in the graph.
    adjacency_matrix = search_diamond(adjacency_matrix)
    nodes_low_degree = []
    #Do the procedure for the remaining nodes.
    for vertex_in_matrix in adjacency_matrix:
        for neighbor_vertex in vertex_in_matrix:
            if math.isnan(neighbor_vertex):
                continue
            else:
                nodes_low_degree.append(vertex_label)
        vertex_label += 1
    print("New graph " + str(nodes_low_degree))
    if len((nodes_low_degree)) < 4:
        print("Remaining nodes can not construct a diamond.")
        print("Graph is diamond-free.")
        draw_and_show()
        exit()

#Close file.
inputFile.close()
