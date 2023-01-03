#Input (0,1,3,4,5,8,9) : Output False
#Input (2,6,7,10,11,12,13) : Output True

#Bfs_recognition

from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

def draw_and_show():
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

def visualization(vertex_name, color_of_vertex):
    colors[int(vertex_name)] = color_of_vertex

def reminder_of_color(current_color,node_for_change,reseting_color):
    reseting_color = " "
    if colors[int(node_for_change)] == current_color:
        reseting_color = current_color
    return reseting_color

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())
    input_node = input("Choose node from 0 to " + str(nodes_num-1) + ": ")

    #Add all nodes in the graph.
    for i in range(nodes_num):
        G.add_node(str(i),color = "#C0C0C0")

    #Store the graph as a dictionary.
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

    return adjacency_list,input_node,pos,colors

def bfs(root):
    #green.
    visualization(root ,"#006633")
    draw_and_show()
    visited_nodes = {}
    level = {}
    L1 = []
    L2 = []
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
    reminder_of_neigh = 0
    Flag_for_level1 = True

    print("root " +str(root))
    while not queue.empty():
        #Store 2 common neighbors between a non-neighbor of root and the root.
        neighbors_of_root = []
        current_node = queue.get()
        if current_node != root and level[current_node]==2:
            #red.
            print("Current node " +str(current_node))
            visualization(current_node,"#FF0000")
            draw_and_show()
        #Mark all vertices at distance two from root.
        if level[current_node] < 3 :
            BFS_output.append(current_node)
            for neighbor in adj_list[current_node]:
                print("Neighbor " +str(neighbor))
                if not visited_nodes[neighbor] :
                    visited_nodes[neighbor] = True
                    level[neighbor] = level[current_node] + 1
                    queue.put(neighbor)
                    if level[neighbor]==1 :
                        #yellow
                        visualization(neighbor,"#FFFF33")
                        L1.append(neighbor)
                    elif level[neighbor]==2:
                        L2.append(neighbor)
                        if Flag_for_level1:
                            print("L1 set " +str(L1))
                            draw_and_show()
                            print("LEVEL 2 ")
                            Flag_for_level1 = False
                            for element_level1 in L1:
                                visualization(element_level1,"#C0C0C0")
                            draw_and_show()
                    else:
                        #Level 3.
                        #orange.
                        visualization(neighbor,"#FF8000")
                        draw_and_show()
                        #grey light.
                        visualization(neighbor,"#C0C0C0")
                        draw_and_show()
                #If a non-neighbor of root(current_node) share a neighbor with root,append neighbor in neighbors_of_root list.
                elif level[current_node]== 2 and level[neighbor]== 1 :
                    neighbors_of_root.append(neighbor)
                    reminder_of_neigh = neighbor
                    #blue light.
                    print("Common node is found: " +str(neighbor))
                    visualization(neighbor, "#6B6BFD")
                    draw_and_show()
            #If neighbors_of_root list store at least 2 nodes,then v_vertex is in an induced diamond or C4.
            if len(neighbors_of_root)==2:
                for element in neighbors_of_root:
                    colors[int(element)] = "purple"
                print("Vertices " + str(root) + "," +str(current_node) + "," +str(neighbors_of_root[0]) + "," +str(neighbors_of_root[1]) + "," + " produce an induced C4 or diamond.")
                return False
            #reset neighbor from blue to grey.
            if colors[int(reminder_of_neigh)] == "#6B6BFD":
                #grey.
                visualization(reminder_of_neigh,"#C0C0C0")
                draw_and_show()
    for elem in L1:
        visualization(elem,"#FFFF33")
    print("L2 set " + str(L2))
    print("Vertex " +str(root) + " is not part of an induced C4 or diamond.")
    draw_and_show()
    return True

###-----------MAIN-----------###

#Variable file name: entered by user at runtime.
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
#Create graph for visualization.
G = nx.Graph()
#Check for unacceptable input node and graph's information and then create the adjacency list.
adj_list,v_vertex,pos,colors = graph_file(inputFile)

result = True
#Breadth first search algorithm starting from v_vertex
#return False if C4 or diamond is found in graph else return True.
result = bfs(v_vertex)
print(result)
draw_and_show()

#close file.
inputFile.close()
