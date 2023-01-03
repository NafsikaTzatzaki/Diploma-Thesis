# Input(graph_1.txt or graph_2.txt) : Output False.
# Input(graph_3.txt) : Output True.

from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

def deleted_nodes(node_for_delete):

    for node_partner in adj_list[node_for_delete]:
        if G.has_edge(str(node_for_delete),str(node_partner)):
            G.remove_edge(str(node_for_delete),str(node_partner))

def erase_colors():
    for node_key in adj_list.keys():
        if colors[int(node_key)] != "#006633" and colors[int(node_key)] != "#202020":
            colors[int(node_key)] = "#C0C0C0"
    draw_and_show()

def draw_and_show():
    nx.draw(G,pos,with_labels = 1,node_color = colors)
    plt.show()

def visualization(vertex_name, color_of_vertex):
    if vertex_name:
        colors[int(vertex_name)] = color_of_vertex

def reminder_of_color(current_color,node_for_change,reseting_color):
    reseting_color = " "
    if colors[int(node_for_change)] == current_color:
        reseting_color = current_color
    return reseting_color

def check_for_reminder(current_color,basic_color,node_for_change,reseting_color):
    if reseting_color == current_color:
        visualization(node_for_change,current_color)
    else:
        colors[int(node_for_change)] = basic_color

def graph_file(file):
    nodes_num = int(file.readline())
    edges_num = int(file.readline())

    adjacency_list = {}
    for readline in file :
        edge = readline.strip()
        nodes_from_edge = edge.split("-")
        node1 = nodes_from_edge[0]
        node2 = nodes_from_edge[1]

        #Add all nodes in the graph.
        for i in range(nodes_num):
            #grey soft.
            G.add_node(str(i),color = "#C0C0C0")

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
        ##
        #Check for duplicate edges.
        if (node1 in adjacency_list[node2]) and (node2 in adjacency_list[node1]):
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
    print("Threshold: " +str(f_threshold))

    #Visualize the graph with all nodes and edges.
    pos = nx.circular_layout(G)
    colors = nx.get_node_attributes(G,'color').values()
    colors = list(colors)
    nx.draw(G,pos,with_labels = 1, node_color=colors)
    plt.show()
    return adjacency_list,nodes_num,f_threshold,pos,colors

def bfs(root):
    #green.
    visualization(root,"#006633")
    draw_and_show()
    visited_nodes = {}
    level = {}
    parent = {}
    #Add L1,L2.
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
                        visualization(neighbor,"#FFFF33")
                    if level[neighbor] == 2:
                        distance_L2.append(neighbor)
                        visualization(neighbor,"#FF8000")
                    queue.put(neighbor)
    if (not distance_L1):
        print("L1 set is empty. Graph is (C4,diamond)-free.")
        exit()
    if (not distance_L2):
        print("L2 set is empty. Graph is (C4,diamond)-free.")
        exit()

    print("L1 set" +str(distance_L1))
    print("L2 set" +str(distance_L2))
    print("Parent dictionary: ")
    for item_parent in parent.items():
        print(item_parent)
    draw_and_show()
    erase_colors()
    return distance_L1,distance_L2,parent,level

def Case_1a(L1):
    #Case 1a: If l1 does not induce a disjoint union of cliques then return no.
    print("Case 1a")
    node_color = ""
    for node_in_L1 in L1:
        #red.
        visualization(node_in_L1,"#FF0000")
        draw_and_show()
        for neighbor_of_node in adj_list[node_in_L1]:
            #orange
            reminder_color = reminder_of_color("#FF0000",neighbor_of_node,reminder_of_color)
            if neighbor_of_node != v_vertex:
                visualization(neighbor_of_node,"#FF8000")
                draw_and_show()
            if neighbor_of_node in L1:
                #pink
                visualization(neighbor_of_node,"#FF8888")
                draw_and_show()
                for neighbor_of_neigh in adj_list[neighbor_of_node]:
                    #reminder_of_color("#FF0000",neighbor_of_neigh,reminder_of_neigh)
                    if neighbor_of_neigh != v_vertex and neighbor_of_neigh != node_in_L1:
                        visualization(neighbor_of_neigh,"#FF8000")
                        draw_and_show()
                    if (neighbor_of_neigh != node_in_L1) and (neighbor_of_neigh in L1):
                        #Yellow
                        visualization(neighbor_of_node,"#FFFF33")
                        draw_and_show()
                        #If a P3 found then return False.
                        if neighbor_of_neigh not in adj_list[node_in_L1]:
                            #purple.
                            visualization(node_in_L1,"#990099")
                            visualization(neighbor_of_node,"#990099")
                            visualization(neighbor_of_neigh,"#990099")
                            print("P3 is found from nodes " + str(node_in_L1) + " " + str(neighbor_of_node) + " " + str(neighbor_of_neigh))
                            print("Graph has an induced C4 or diamond.")
                            draw_and_show()
                            return False
                        else:
                            visualization(neighbor_of_neigh,"#C0C0C0")
                            draw_and_show()
                    if colors[int(neighbor_of_neigh)]=="#FF8000":
                            visualization(neighbor_of_neigh,"#C0C0C0")
                            draw_and_show()
                #pink #soft grey
                check_for_reminder("#FF0000","#C0C0C0",neighbor_of_node,reminder_color)
            if colors[int(neighbor_of_node)]=="#FF8000":
                visualization(neighbor_of_node,"#C0C0C0")
                draw_and_show()
    draw_and_show()
    print("P3 didn't found.")
    print("L1 set induces a disjoint union of cliques.")
    erase_colors()
    return True

def Case_1b(L1,L2):

    #Case 1b: If a vertex in l2 sees two or more vertices in l1 then return no.
    print("Case 1b")
    for item_in_L2 in L2:
        #red.
        visualization(item_in_L2,"#FF0000")
        draw_and_show()
        counter_two_vertices = 0
        for neighbor_of_item_L2 in adj_list[item_in_L2]:
            if counter_two_vertices < 2 :
                reminder_color = reminder_of_color("#FF0000",neighbor_of_item_L2,reminder_of_color)
                #orange.
                visualization(neighbor_of_item_L2,"#FF8000")
                draw_and_show()
                if neighbor_of_item_L2 in L1:
                    counter_two_vertices += 1
                    #pink.
                    visualization(neighbor_of_item_L2,"#FF8888")
                    draw_and_show()
                check_for_reminder("#FF0000","#C0C0C0",neighbor_of_item_L2,reminder_color)
            else:
                return False
        for neighbor_of_item_L2 in adj_list[item_in_L2]:
            if colors[int(neighbor_of_item_L2)]!= "#FF0000":
                colors[int(neighbor_of_item_L2)] = "#C0C0C0"
        draw_and_show()
    print("None vertex from L2 sees two or more vertices from L1.")
    erase_colors()
    return True

def Case_1c(L1,L2):
    """Case 1c: For each vertex wεL1 do
                 if N(w)ՈL2 does not induce a disjoint union of cliques then return no."""
    print("Case 1c")
    for item_in_L1 in L1:
        #dark green.
        visualization(item_in_L1,"#09642A")
        #Find intersection of N(w) Λ L2.
        set_intersect = []
        for neighbor in adj_list[item_in_L1]:
            if neighbor in L2:
                set_intersect.append(neighbor)
        print("Intersection set " + str(set_intersect))
        #light green.
        for item_of_intersect in set_intersect:
            colors[int(item_of_intersect)] = "#34C168"
        draw_and_show()
        #Check if intersection of N(w) Λ L2 does not induce a disjoint union of cliques.
        for node_in_intersect in set_intersect:
            #red.
            visualization(node_in_intersect,"#FF0000")
            draw_and_show()
            for neighbor_of_node in adj_list[node_in_intersect]:
                if neighbor_of_node in set_intersect:
                    if colors[int(neighbor_of_node)]=="#FF0000":
                        #pink.
                        visualization(neighbor_of_node,"#FF8888")
                        draw_and_show()
                        #red.
                        visualization(neighbor_of_node,"#FF0000")
                        draw_and_show()
                    else:
                        #pink.
                        visualization(neighbor_of_node,"#FF8888")
                        draw_and_show()
                    for neighbor_of_neigh in adj_list[neighbor_of_node]:
                        if neighbor_of_neigh!=node_in_intersect:
                            #If a P3 found then return False.
                            if (neighbor_of_neigh in set_intersect) and (neighbor_of_neigh not in adj_list[node_in_intersect]):
                                #purple.
                                print("Graph has an induced C4 or diamond.")
                                visualization(neighbor_of_neigh,"#990099")
                                draw_and_show()
                                return False
        if set_intersect:
            print("Intersection set induces a disjoint union of cliques.")
        else:
            print("Intersection set is empty.")
        erase_colors()
    return True

def Case_1d(L2,parent):
    """Case 1d : For each edge xy with xεL2 and yεL2 do
                   Let x' = parent(x) and  y' = parent(y)
                   if x'sees y' then return no. """
    print("Case 1d")
    #Store items from L2 so as to avoid repeats(xy -> yx).
    items_array = []
    for item_in_L2 in L2:
        #yellow.
        items_array.append(item_in_L2)
        visualization(item_in_L2,"#FFFF33")
        draw_and_show()
        reset_itemL2 = reminder_of_color("#FFFF33",item_in_L2,reminder_of_color)
        for neighbor in adj_list[item_in_L2]:
            if neighbor not in items_array:
                reset_neighbor = reminder_of_color("#FFFF33",neighbor,reminder_of_color)
                #pink.
                visualization(neighbor,"#FF8888")
                draw_and_show()
                if neighbor in L2:
                    print("Edge from vertices " +str(item_in_L2) + "," +str(neighbor))
                    reset_neighbor = reminder_of_color("#FFFF33",neighbor,reminder_of_color)
                    #blue light.
                    visualization(neighbor,"#3399FF")
                    visualization(item_in_L2,"#3399FF")
                    draw_and_show()
                    reset_parent1 = reminder_of_color("#FFFF33",parent[item_in_L2],reminder_of_color)
                    #blue.
                    print("Parent of vertex "+ str(item_in_L2) + " is vertex " +str(parent[item_in_L2]))
                    visualization(parent[item_in_L2],"#0000FF")
                    print("Parent of vertex "+ str(neighbor) + " is vertex " +str(parent[neighbor]))
                    visualization(parent[neighbor],"#0000FF")
                    draw_and_show()
                    if parent[item_in_L2] is adj_list[parent[neighbor]]:
                        #red.
                        visualization(parent[item_in_L2],"#FF0000")
                        visualization(parent[neighbor],"#FF0000")
                        print("Parent " + str(parent[item_in_L2]) + " sees parent " +str(parent[neighbor]))
                        print("Graph has an induced C4 or diamond.")
                        draw_and_show()
                        return False
                    else:
                        print("Parent " + str(parent[item_in_L2]) + " doesn't see parent " +str(parent[neighbor]))
                        reset_parent2 = reminder_of_color("#FFFF33",parent[neighbor],reminder_of_color)
                        #blue.
                        visualization(parent[neighbor],"#0000FF")
                        draw_and_show()
                    visualization(parent[item_in_L2],"#C0C0C0")
                    visualization(parent[neighbor],"#C0C0C0")
                    visualization(neighbor,"#C0C0C0")
                    visualization(item_in_L2,"#FFFF33")
                else:
                    visualization(neighbor,"#C0C0C0")
        visualization(item_in_L2,"#C0C0C0")
        draw_and_show()
    erase_colors()
    print("None edge xy with x,yεL2,x'= parent(a),y'= parent(b) such that x'sees y' is found.")
    return True

def Case_1e(L2,parent):
    #Case 1e: If xεL2 sees aεL2 and bεL2 such that parent(a)=parent(b),but parent(x)!= parent(b) then return no.
    print("Case 1e")
    for item_in_L2 in L2:
        a_vertex = None
        b_vertex = None
        #yellow.
        visualization(item_in_L2,"#FFFF33")
        draw_and_show()
        for neighbor in adj_list[item_in_L2]:
            #pink.
            if neighbor in L2:
                if a_vertex == None:
                    print("Vertex "+str(item_in_L2)+ " sees vertex "+str(neighbor))
                    a_vertex = neighbor
                    #pink.
                    visualization(a_vertex,"#FF8888")
                    draw_and_show()
                else:
                    b_vertex = neighbor
                    print("Vertex " +str(item_in_L2)+ " sees vertices "+str(a_vertex)+ " and "+str(b_vertex))
                    #pink.
                    visualization(b_vertex,"#FF8888")
                    draw_and_show()
                    if parent[a_vertex]==parent[b_vertex]:
                        visualization(parent[a_vertex],"#0000FF")
                        if parent[item_in_L2]!=parent[a_vertex]:
                            print("Vertices " +str(a_vertex)+ " and "+str(b_vertex)+ " have the same parent " +str(parent[a_vertex]) +" but different from node " +str(item_in_L2))
                            print("Graph has an induced C4 or diamond.")
                            visualization(parent[item_in_L2],"#FF0000")
                            visualization(parent[a_vertex],"#FF0000")
                            draw_and_show()
                            return False
                        else:
                            visualization(parent[a_vertex],"#C0C0C0")
                            print("Vertices "+str(item_in_L2)+ "," +str(a_vertex)+ "," +str(b_vertex) +" have the same parent " +str(parent[a_vertex]))
                            draw_and_show()
                    else:
                        print("Vertices "+str(a_vertex)+ "," +str(b_vertex) +" have different parents.")
                        visualization(b_vertex,"#C0C0C0")
                        draw_and_show()
        visualization(a_vertex,"#C0C0C0")
        visualization(item_in_L2,"#C0C0C0")
        draw_and_show()
    print("None vertex of L2 sees two vertices a,b such that parent(a)==parent(b) but parent(x)!=parent(b).")
    return True

def Case_1f(L2,parent):
    #Case 1f: If xεL2 sees aεL2 and bεL2 such that parent(a)=parent(b) then return no.
    print("Case 1f")
    for item_in_L2 in L2:
        a_vertex = None
        b_vertex = None
        #yellow.
        visualization(item_in_L2,"#FFFF33")
        draw_and_show()
        for neighbor in adj_list[item_in_L2]:
            #pink.
            if neighbor in L2 :
                if a_vertex == None:
                    print("Vertex "+str(item_in_L2)+ " sees vertex "+str(neighbor))
                    a_vertex = neighbor
                    #pink.
                    visualization(a_vertex,"#FF8888")
                    draw_and_show()
                else:
                    b_vertex = neighbor
                    print("Vertex " +str(item_in_L2)+ " sees vertices "+str(a_vertex)+ " and "+str(b_vertex))
                    #pink.
                    visualization(b_vertex,"#FF8888")
                    draw_and_show()
                    if parent[a_vertex]==parent[b_vertex]:
                        print("Vertices " +str(a_vertex)+ " and "+str(b_vertex)+ " have the same parent " +str(parent[a_vertex]))
                        print("Graph has an induced C4 or diamond.")
                        #red.
                        visualization(parent[a_vertex],"#FF0000")
                        draw_and_show()
                        return False
                    else:
                        print("Vertices "+str(a_vertex)+ "," +str(b_vertex) +" have different parents.")
                        visualization(b_vertex,"#C0C0C0")
                        draw_and_show()
        visualization(a_vertex,"#C0C0C0")
        visualization(item_in_L2,"#C0C0C0")
        draw_and_show()
    print("None vertex of L2 sees two vertices a,b such that parent(a)==parent(b).")
    return True

def elimination(node):
    #Perform breadth-first search from v until all vertices at distance 3 from v are marked.
    L1_list,L2_list,parent_list,level_list = bfs(node)

    #Change for testing visualization.
    result_from_case = True
    result_from_case = Case_1a(L1_list)
    #If result_from_case is True then continue to check next case else return False.
    if result_from_case:
        result_from_case = Case_1b(L1_list,L2_list)
    if result_from_case:
        result_from_case = Case_1c(L1_list,L2_list)
    if result_from_case:
        result_from_case = Case_1d(L2_list,parent_list)
    if result_from_case:
        result_from_case = Case_1e(L2_list,parent_list)
    if result_from_case:
        result_from_case = Case_1f(L2_list,parent_list)

    #If the result of last case is True then delete N(u)U{u} from the graph and update the degrees of the remaining vertices.
    if result_from_case:
        for neighbor_node in adj_list[node]:
            deleted_nodes(neighbor_node)
            colors[int(neighbor_node)] = "#202020"
            adj_list.pop(neighbor_node)
        for neighbors in adj_list.values():
            for vertex in neighbors:
                if vertex not in adj_list.keys():
                    neighbors.remove(vertex)
        colors[int(node)] = "#202020"
        adj_list.pop(node)
        for key,value in list(adj_list.items()):
            if len(adj_list[key])==0:
                colors[int(key)] = "#202020"
                adj_list.pop(key)
    if len(adj_list) < 4:
        print("Remaining vertices are less than 4. C4 or diamond can not be constructed.")
        print("Graph is (C4,diamond)-free.")
        print("False")
        draw_and_show()
        exit()
    return result_from_case

def recognition_bfs(root):
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
    #root.
    visited_nodes[root] = True
    level[root] = 0
    queue.put(root)
    current_node = None
    level[current_node]=0
    reminder_of_neigh = 0
    Flag_for_level1 = True

    while not queue.empty():
        #Store 2 common neighbors between a non-neighbor of root and the root.
        neighbors_of_root = []
        current_node = queue.get()
        if current_node != root and level[current_node]==2:
            print("Current node " +str(current_node))
            #red.
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
                draw_and_show()
                print("Vertices " + str(root) + "," +str(current_node) + "," +str(neighbors_of_root[0]) + "," +str(neighbors_of_root[1]) + "," + " produce an induced C4 or diamond.")
                return False
            #reset neighbor from blue to yellow.
            if colors[int(reminder_of_neigh)] == "#6B6BFD":
                #grey.
                visualization(reminder_of_neigh,"#C0C0C0")
                draw_and_show()
    print("L2 set " + str(L2))
    print("Vertex " +str(root) + " is not part of an induced C4 or diamond.")
    draw_and_show()
    return True

###-----------MAIN-----------###

#Variable file name: entered by user at runtime
fileName = input("Enter name of file: ")
inputFile = open(fileName, "r")

#Create graph for visualization.
G = nx.Graph()
adj_list,nodes_num,threshold,pos,colors = graph_file(inputFile)

#Find Δ(G)(maximum vertex degree in graph).
max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
print("Δ(G): " +str(max_degree))

result = True
#Loop while Δ(G) is above the threshold f.
while max_degree > threshold:
    for key,value in list(adj_list.items()):
        #Find a vertex v of degree Δ(G).
        if len(value) == max_degree:
            v_vertex = key
            # Function 'elimination' check all possible case so as to find C4 or diamond in graph.
            # If a case return False then print False and exit() because graph contains C4 or diamond.
            # If all cases return True then Function 'elimination' eliminate v and N(v)(neighbors of v) from consideration.
            print("Node of degree Δ(G): " + str(v_vertex))
            result = elimination(v_vertex)
            if result:
                print("Previous Δ(G): " +str(max_degree))
                max_degree = max(len(adj_list[vertex]) for vertex in adj_list)
                print("New Δ(G): " +str(max_degree))
                break
            else:
                print("C4 or diamond is found.")
                print("result " + str(result))
                exit()

#If Δ(G) <= threshold f and result_from_case is True then run OmD algorithm for each node for the remaining graph.
print("Δ(G) "+str(max_degree)+ "of the remaining graph doesn't exceed threshold " + str(threshold))
for node in adj_list:
    print("Run algorithm  3.1 for node "+str(node))
    result = recognition_bfs(node)
    #If the result from OmD algorithm is True then continue to next node else break and print False.
    if not result:
        break
if result:
    print("Graph is (C4,diamond)-free.")
    print("result " + str(result))
inputFile.close()
