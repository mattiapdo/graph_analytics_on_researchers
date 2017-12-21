from collections import deque

'''...Some usefull fuctions for the code...'''
#function tu remove duplicate from list of dictionaries
def setDict(L):    
    D = dict()
    for l in L: D[l['author_id']] = l
    output = list(D.values())
    return output

#function to remove element of the second list from the first list
def Remove(L1, L2):
    return [x for x in L1 if x not in L2]
    
#function to compute the jaccard similarity between two sets of publication
def J(p1, p2):
    return len(set(p1).intersection(p2))/len(set(p1).union(p2))

#recursive version which could raise RecursionError: maximum recursion depth exceeded while calling a Python object
#for deep searchs

#function to implement the breath first traversal and return a dictionary with all nodes as keys and the number of hop from source to the node as values 
def bfsr(G, source, d, OUTPUT = {}, TO_VISIT = deque([]), hop = 0, flag = 1):
    #OUTPUT = {1:0}: dictionary of nodes already visited, key node and value the number of hops to get there from the source
    #TO_VISIT = deque([]): FIFO queue of nodes to visit
    
    #if first iteration add the source with 0 as number of hops
    if (flag == 1):
        OUTPUT[source] = 0
        flag = 0
        
    #if no neighbor or all neighbors already visited
    if len (G.neighbors(source)) == 0 or len([e for e in G.neighbors(source) if e in OUTPUT.keys()]) == len(G.neighbors(source)): 
        return OUTPUT
    
    for neighbor in G.neighbors(source):
        #add them into the To_VISIT queue and into the visited nodes
        if (neighbor not in OUTPUT.keys()):
            TO_VISIT.append((neighbor, hop+1))
            OUTPUT[neighbor] = hop+1
        
    #while there is something to visit
    while(len(TO_VISIT) != 0):
        #remove the first element from the queue and visit it (FIFO)
        node = TO_VISIT.popleft()
        
        if (node[1] + 1 <= d):
            bfsr(G, node[0], d, OUTPUT, TO_VISIT, node[1], flag = 0)
        
    #we are done visiting everything so we can return the output dictionary
    return OUTPUT

  
#iterative version
#function to implement the breath first traversal and return a dictionary with all nodes as keys and the number of hop from source to the node as values 
def bfsi(G, source, d = 0, OUTPUT = {}, TO_VISIT = deque([])):
    #OUTPUT = {1:0}: dictionary of nodes already visited, key node and value the number of hops to get there from the source
    #TO_VISIT = deque([]): FIFO queue of nodes to visit
    
    hop = 0
    OUTPUT[source] = 0
    
    #if no neighbor or all neighbors already visited
    if len (G.neighbors(source)) == 0 or len([e for e in G.neighbors(source) if e in OUTPUT.keys()]) == len(G.neighbors(source)): 
        pass
    else:
        for neighbor in G.neighbors(source):
            #add them into the To_VISIT queue and into the visited nodes
            if (neighbor not in OUTPUT.keys()):
                TO_VISIT.append((neighbor, hop+1))
                OUTPUT[neighbor] = hop+1
        
    #while there is something to visit
    while(len(TO_VISIT) != 0):
        #remove the first element from the queue and visit it (FIFO)
        node = TO_VISIT.popleft()
        
        if (node[1] + 1 <= d):
            #if no neighbor or all neighbors already visited
            if len (G.neighbors(node[0])) == 0 or len([e for e in G.neighbors(node[0]) if e in OUTPUT.keys()]) == len(G.neighbors(node[0])): 
                pass
            else:
                for neighbor in G.neighbors(node[0]):
                    #add them into the To_VISIT queue and into the visited nodes
                    if (neighbor not in OUTPUT.keys()):
                        TO_VISIT.append((neighbor, node[1]+1))
                        OUTPUT[neighbor] = node[1]+1
                        
                    
    #we are done visiting everything so we can return the output dictionary
    return OUTPUT


#function to compute the shortest path weight from a source node to a destination
#this function is just an addaptation of the bfsi function above
def shortest_path(G, source, destination):
    #OUTPUT = {1:0}: dictionary of nodes already visited, key node and value the number of hops to get there from the source
    #TO_VISIT = deque([]): FIFO queue of nodes to visit
    
    weight = 0
    OUTPUT = {}
    OUTPUT[source] = 0
    TO_VISIT = deque([])
    
    #if no neighbor
    if len (G.neighbors(source)) == 0: 
        pass
    else:
        for neighbor in G.neighbors(source):
            #add them into the To_VISIT queue and into the visited nodes
            if (neighbor not in OUTPUT.keys()):
                TO_VISIT.append((neighbor, weight + G.edge[source][neighbor]['weight']))
                OUTPUT[neighbor] = weight + G.edge[source][neighbor]['weight']
        
    #while there is something to visit
    while(len(TO_VISIT) != 0):
        #remove the first element from the queue and visit it (FIFO)
        node = TO_VISIT.popleft()
        
        #if no neighbor
        if len (G.neighbors(node[0])) == 0: 
            pass
        else:
            for neighbor in G.neighbors(node[0]):
                #add them into the To_VISIT queue and into the visited nodes
                #if the neighbor is not visited yet add it into the to visited queue and into the already visited dictionary
                if (neighbor not in OUTPUT.keys()):
                    TO_VISIT.append((neighbor, node[1]+G.edge[node[0]][neighbor]['weight']))
                    OUTPUT[neighbor] = node[1]+G.edge[node[0]][neighbor]['weight']
                #if the neighbor is yet visited, check if the actual weight is less than the old one and replace if it does
                else:
                    if (node[1]+G.edge[node[0]][neighbor]['weight'] < OUTPUT[neighbor]):
                        TO_VISIT.append((neighbor, node[1]+G.edge[node[0]][neighbor]['weight']))
                        OUTPUT[neighbor] = node[1]+G.edge[node[0]][neighbor]['weight']
                    
    #we are done visiting everything so we can return the output dictionary
    if destination in OUTPUT.keys():
        return OUTPUT[destination]
    else:
        return None
    

#This function takes in input a graph, a set/list of nodes and returns the dictionary
#which contains all the nodes of the graph as keys and the shortest path from u to the other nodes of the graph
#as values, for each u in nodes_set'''
def GroupNumbers(G, nodes_set):

    #OUTPUT dictionary: structure {author_id1:(shortest_path, corresponding node in I), ...}
    OUTPUT = {}
    #for all nodes in the graph
    for v in G.nodes():
        #initialise the output: shortest paths to infinity and the corresponding nodes to None
        OUTPUT[v] = (float('inf'), None)
    
    #for all nodes in list of nodes
    for u in nodes_set:
        
        TO_VISIT = deque([])
        OUTPUT[u] = (0, u)
        
        #if no neighbor
        if len (G.neighbors(u)) == 0: 
            pass
        else:
            for neighbor in G.neighbors(u):
                
                #add them into the To_VISIT queue and into the visited nodes
                if (OUTPUT[u][0]+G.edge[u][neighbor]['weight'] < OUTPUT[neighbor][0]):
                    TO_VISIT.append((neighbor, OUTPUT[u][0]+G.edge[u][neighbor]['weight']))
                    OUTPUT[neighbor] = (OUTPUT[u][0]+G.edge[u][neighbor]['weight'], u)
                        
        #while there is something to visit
        while(len(TO_VISIT) != 0):
            #remove the first element from the queue and visit it (FIFO)
            node = TO_VISIT.popleft()
            
            #if no neighbor
            if len (G.neighbors(node[0])) == 0: 
                pass
            else:
                for neighbor in G.neighbors(node[0]):
                    #add them into the To_VISIT queue and into the visited nodes
                        if (node[1]+G.edge[node[0]][neighbor]['weight'] < OUTPUT[neighbor][0]):
                            TO_VISIT.append((neighbor, node[1]+G.edge[node[0]][neighbor]['weight']))
                            OUTPUT[neighbor] = (node[1]+G.edge[node[0]][neighbor]['weight'], u)
            
    return OUTPUT
