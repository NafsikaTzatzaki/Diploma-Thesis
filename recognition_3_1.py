#Input (0,1,3,4,5,8,9) : Output False
#Input (2,6,7,10,11,12,13) : Output True

from queue import Queue

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())
    input_node = input("Choose node from 0 to " + str(nodes_num-1) + ": ")

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
    #Check if edges is at least nodes-1.
    if edges_num < (nodes_num-1):
        print("Statement edges >= (nodes-1) is violated.")
        exit()

    return adjacency_list,input_node

def bfs(root):

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
                #If a non-neighbor of root(current_node) share a neighbor with root,
                #append neighbor in neighbors_of_root list.
                elif level[current_node]== 2 and level[neighbor]== 1 :
                    neighbors_of_root.append(neighbor)
            #If neighbors_of_root list store at least 2 nodes,
            #then v_vertex is in an induced diamond or C4.
            if len(neighbors_of_root)>=2:
                print("C4 or diamond is found.")
                return False
    return True

###-----------MAIN-----------###

#Variable file name: entered by user at runtime.
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")
adj_list,v_vertex = graph_file(inputFile)

result = True
#Breadth first search algorithm starting from v_vertex.
#Return False if C4 or diamond is found in graph else return True.
result = bfs(v_vertex)
print(result)

#close file.
inputFile.close()
