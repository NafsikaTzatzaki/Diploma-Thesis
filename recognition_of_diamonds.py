from queue import Queue
from numpy.linalg import matrix_power
import numpy as np
import math

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

def function_phase_2(matrix,vertex_x):
    #Calculate adjacency_matrix x adjacency_matrix.
    adjacency_matrix_2 = np.zeros((num_of_nodes,num_of_nodes))
    for i in range(num_of_nodes):
        for j in range(num_of_nodes):
            for k in range(num_of_nodes):
                adjacency_matrix_2[i][j] += adjacency_matrix[i][k] * adjacency_matrix[k][j]
    for clique in stored_cliques:
        size_of_clique = len(clique)
        for vertex_1 in clique:
            for vertex_2 in clique:
                if vertex_1 != vertex_2:
                    if adjacency_matrix_2[vertex_1][vertex_2] > (size_of_clique - 1):
                        #Producing a diamond.
                        for item in range(num_of_nodes):
                            if adjacency_matrix[vertex1][item] and adjacency_matrix[vertex2][item] and not adjacency_matrix[vertex][item]:
                                print("These Vertices produce a diamond ", + str(vertex_x) + " " + str(vertex1) + " " + str(vertex2) + " " +str(item))
                        exit()

def check_for_clique(vertex,component,array_of_cliques):
    Flag_for_clique = True
    for element_1 in component:
        for element_2 in component:
            if element_1 !=element_2 :
                #if element_1 and element_2 from set of components are not neighbors.
                if not adjacency_matrix[element_1][element_2]:
                    Flag_for_clique = False
                    result_from_BFS,BFS_output = bfs(element_1,element_2,component)
                    #if result from Breadth First Search is True then a P(3) is found.
                    if result_from_BFS:
                        BFS_output.append(vertex)
                        print("BFS_output PATH IS FOUND " + str(BFS_output))
                        exit()
    #Ιf flag is True then component is a clique and add it in a list.
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
        if degree_of_vertex > 0 and degree_of_vertex <= low_degree:
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
        #Compute the components of the neighborhood of vertex.
        while neighbors_array:
            #Set to keep track of visited nodes of graph.
            visited_list = set()
            #Function dfs(Depth First Search) calculates and returns a component.
            component = dfs(visited_list,neighbors_array[0],neighbors_array[0],neighbors_array)
            #Remove the nodes of the component so as to avoid duplicate compoments.
            for item in component:
                neighbors_array.remove(item)
            #Function check_for_clique checks if the component is a clique.
            stored_cliques = check_for_clique(vertex,component,stored_cliques)
        #Function function_phase_2 for checking Phase 2 of the algorithm if we have cliques in neighborhood of vertex.
        if stored_cliques:
            function_phase_2(adjacency_matrix,vertex)
    #Remove all nodes of low degree from the graph.
    for neighbor_of_low_vertex in range(num_of_nodes):
        for low_degree_vertex in nodes_low_degree:
            adjacency_matrix[low_degree_vertex][neighbor_of_low_vertex] = None
            adjacency_matrix[neighbor_of_low_vertex][low_degree_vertex] = None
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
        adj_matrix[node1][node2] = 1
        adj_matrix[node2][node1] = 1

    #Check if edges >= (nodes-1).
    #Check if edges is at least nodes-1.
    if edges_num < (nodes_num-1):
        print("Statement: edges >= (nodes-1) is violated.")
        exit()
    return adj_matrix,nodes_num,max_low_degrees

###-----------MAIN-----------###

#Variable file name: entered by user at runtime.
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Check for unacceptable input node and graph's information and then create the adjacency list.
adjacency_matrix,num_of_nodes,low_degree = graph_file(inputFile)

#Store all cliques of the neighborhoods of low degree vertices.
stored_cliques = []
#Store low degree vertices in a list .
nodes_low_degree = find_vertex_degree()
#Do the procedure as long as there are nodes in the graph.
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
    exit()

#Close file.
inputFile.close()
