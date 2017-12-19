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
        
        if (node[1] + 1 <= 2):
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
        
        if (node[1] + 1 <= 2):
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

#this version of the shortest path computation function follows the Dijkstra's logic
def our_dijkstra(G, source, goal):
    
    for node in G.nodes():
        #set all nodes as not visited  - creating an apposite attribute
        G.node[node]['visited'] = False
        #set, for all nodes the tentative distance as infinity
        G.node[node]['tentative_dist'] = float("inf")
        
    
    import heapq as hp
    # set current node on source node
    current = source
    #print('current', current)
    # set source node as visited
    G.node[current]['visited'] = True
    #print("G.node[current]['visited']", current)
    # set the tentative distance of current node (source) as zero
    G.node[current]['tentative_dist'] = float(0)
    #print("tentative_dist", G.node[current]['tentative_dist'])
    #here a heap that contains tuples: for each node we have:
    #(tentative distance from source, node id)
    #tentatives = [(G.node[current]['tentative_dist'], current)]
    tentatives = []
    #print('tentatives', tentatives)
    #print('courrent', current, 'neigh', list(G.neighbors(current)))
    # while current node has neighbours and current node is not our goal node...
    while G.neighbors(current) and current != goal:
        #print('current', current)
        for neighbour in list(G.neighbors(current)):
            #print('\tneighbour', neighbour, 'visitato?', G.node[neighbour]['visited'])
            #if neighbour has NOT been visited:
            if G.node[neighbour]['visited'] == False:
                # set his tentative distance as the minimum between
                # its pre-stored tentative distance and 
                # the sum of current's tentative distance and the weigth that links current with neighbour
                
                '''print('\t\t', 
                     G.node[neighbour]['tentative_dist'],'\n\t\t',
                     G.node[current]['tentative_dist']+ G[current][neighbour]['weight'])'''
                                                          
                G.node[neighbour]['tentative_dist'] = min(G.node[neighbour]['tentative_dist'], 
                                                          G.node[current]['tentative_dist']+
                                                          G[current][neighbour]['weight'])
                #print(G.node[neighbour]['tentative_dist'])
                # push the updated tentative distance in tentatives in the following format:
                # ( updated tentative distance , neighbour )
                hp.heappush(tentatives, (G.node[neighbour]['tentative_dist'], neighbour))
                
        #print('*')
        #print('tentatives: ',tentatives)
        current = hp.heappop(tentatives)[1]
        G.node[current]['visited'] = True
    # the shortest path's distance between source node and goal node is the tentative distance
    # of the goal node
    return G.node[goal]['tentative_dist']
    

def GroupNumbers(G, I):
    OUTPUT = {}
    
    for node in G.nodes():
        sp = [shortest_path(G, node, u) for u in I]
        OUTPUT[node] = min(i for i in sp if i is not None)
        
    return OUTPUT
