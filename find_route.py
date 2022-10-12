''' Artificial Intelligence 
    PROJECT-1
    TASK1
    Name: Somu LeelaMadhav 
    ID: 1002028333'''

import sys
from queue import PriorityQueue

# Function to read the files and to construct based on the text files from typing import Dict, List, Tuple.

def readInputfile(input_data):
    tree= {}
    heuristic = {}
    if input_data==sys.argv[1]:
        read_file = open(input_data,'r')
        data = read_file.readlines()
        read_file.close()
        for line in data[:-1]:
                nodes = line.split()
                if(nodes[0] in tree):#if first node is in tree, append 
                    tree[nodes[0]].append((int(nodes[2]), nodes[1]))
                else:
                    tree[nodes[0]]=[(int(nodes[2]), nodes[1])]
                if(nodes[1] in tree):
                    tree[nodes[1]].append((int(nodes[2]), nodes[0]))
                else:
                    tree[nodes[1]]=[(int(nodes[2]), nodes[0])]
        return tree
    elif input_data==sys.argv[4]: #Consider the heuristic file 
        read_file = open(input_data,'r')#read the input_data
        data = read_file.readlines()
        read_file.close()
        for line in data[:-1]:
            nodes = line.split()#split line
            heuristic[nodes[0]] = int(nodes[1])
        return heuristic#return the heuristic which we got
    
    
    
# Function to perform A* search
def AStar_Search(search_tree, start, goal, heuristic):
    expanded_nodes = 0
    nodes_generate = 1 
    closed_set = []
    fringe_set = PriorityQueue()
    fringe_set.put([0, start])
    while not fringe_set.empty():#Running the loop until fringe is empty
        expanded_nodes+=1
        position = fringe_set.get()
        if position[-1]==goal:#Destination/goal is observed, then return the values which are required.
            return expanded_nodes, nodes_generate,len(closed_set), position
        else:
            if position[-1] not in closed_set:#if previous position is not in closed set, append it
                closed_set.append(position[-1])
                for i in search_tree[position[-1]]:
                    nodes_generate+=1
                    fringe_set.put([i[0]+heuristic[i[1]],position[1:], i[1]])#Include the cost with the heuristic value as g(n)+h(n)
    return expanded_nodes, nodes_generate,len(closed_set),None


# Function to perform UFS ( Uniform cost search )
def UC_Search(search_tree, start, goal):
    expanded_nodes = 0
    nodes_generated = 1
    closed_set = []
    fringe_set = PriorityQueue()
    fringe_set.put([0, start])
    while not fringe_set.empty():#While fringe set is not empty
        expanded_nodes+=1
        position = fringe_set.get()
        if position[-1]==goal:
            return expanded_nodes, nodes_generated,len(closed_set), position#Return the expanded nodes, nodes generated and position
        else:
            if position[-1] not in closed_set:#previous position is not in closed set
                closed_set.append(position[-1])
                for i in search_tree[position[-1]]:
                    nodes_generated+=1
                    fringe_set.put([position[0]+i[0],position[1:], i[1]])
    return expanded_nodes, nodes_generated, len(closed_set),None  #Now return expanded_nodes, nodes_generated



# Listing routes in the path we have
route_list = []


def list_routes(route_1):
        for i in route_1:
            if type(i) == list:
                list_routes(i)#List routes
            else:
                route_list.append(i)#Now append route_list
        return route_list#return the list of routes

# Making a tree Without Heuristic
if len(sys.argv)==4:
    make_tree = readInputfile(sys.argv[1])
    start = sys.argv[2]
    goal = sys.argv[3]
    expanded_nodes, generated_nodes,popped_nodes, route = UC_Search(make_tree,start,goal)
# Making a tree With Heuristic
elif len(sys.argv)==5:
    make_tree = readInputfile(sys.argv[1])
    start = sys.argv[2]
    goal = sys.argv[3]
    heuristic = readInputfile(sys.argv[4])#read input file and consider as heuristic
    expanded_nodes, generated_nodes,popped_nodes, route = AStar_Search(make_tree,start,goal,heuristic)

else:
    print("The number of arguments are invalid\n Please provide correct number of arguments\n")

print("expanded nodes:"+str(popped_nodes))
print("popped nodes:" + str(expanded_nodes))
print('generated nodes:' + str(generated_nodes))
if route == None:
	print('distance : infinity')
	print('route : none')
else:
    print("distance: " + str(route[0]) + "km")
    print('route:')
    route_list = list_routes(route[1])
    route_list.append(route[2])
    for i in range(len(route_list)-1):
        for j in make_tree[route_list[i]]:
            if(j[1]==route_list[i+1]):
                route_dist = j[0]
        print(str(route_list[i]) + " to "+  str(route_list[i+1]) + " = " + str(route_dist) + "km")



 




