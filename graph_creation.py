import time
start_time = time.time()

'''...importing some usefull library...'''
import json
import networkx as nx
import matplotlib.pyplot as plt
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

 

def GroupNumbers(G, I):
    OUTPUT = {}
    
    for node in G.nodes():
        sp = [shortest_path(G, node, u) for u in I]
        OUTPUT[node] = min(i for i in sp if i is not None)
        
    return OUTPUT

    
'''...The code...''' 
###first question

#creation of an empty graph G
G = nx.Graph()

#dictionary of authors that will be added in the graph after populating it
#structure:
# {author_id_1: authordict1
#  author_id_1: authordict1
#  .
#  .
#  .
#  }
AUTHORS_TO_INSERT = {}


#inverted index dictionary that contains as keys Authors and as values neighbours, publications and conferences
#structure:
# {author_id_1: [[neighbour_id_1, neighbour_id_2, neighbour_id_3,...], [publication_id_1, publication_id_2,...], [conference_id_1, conference_id_2,...]]
#  author_id_2: [[neighbour_id_1, neighbour_id_2, neighbour_id_3,...], [publication_id_1, publication_id_2,...], [conference_id_1, conference_id_2,...]]
#  .
#  .
#  .
#    }
AUTHORS_NEIGHBOURS = {}


#let's take the data from the json file
with open('reduced_dblp.json') as json_data:
    data = json.load(json_data)
    
    
    # for each conference in the json file
    for conference in data:
        
        #for each author in this conference
        for author in conference['authors']:
            #if the author is not yet in the list of authors to insert
            if author not in AUTHORS_TO_INSERT.values():
                #insert it into the list of authors to insert
                AUTHORS_TO_INSERT[author['author_id']] = author
                
            #if authors already in inverted index
            if author['author_id'] in AUTHORS_NEIGHBOURS.keys():
                #update the value with key author in the sort of inverted index dictionary
                #we add all the authors in the actual conference into the list of neighbours removing duplicates
                AUTHORS_NEIGHBOURS[author['author_id']] = [ AUTHORS_NEIGHBOURS[author['author_id']][0] + Remove([elem['author_id'] for elem in conference["authors"]], [author['author_id']]), list(set(AUTHORS_NEIGHBOURS[author['author_id']][1] + [conference['id_publication_int']])), list(set(AUTHORS_NEIGHBOURS[author['author_id']][2] + [conference['id_conference_int']])) ]
                #if authors not already in inverted index
            else:
                #add author in inverted index setting the list of neighbours to all the authors in the actual conference removing duplicates
                AUTHORS_NEIGHBOURS[author['author_id']] = [[author['author_id'] for author in setDict(Remove(conference["authors"], [author]))], [conference['id_publication_int']], [conference['id_conference_int']] ]
    
    
    #now let's insert the the AUTHORS_TO_INSERT in the graph as nodes or vertices
    for author in AUTHORS_TO_INSERT.values():
        G.add_node(author['author_id'], **author)


    #now let's create all the edges using the inverted index (AUTHORS_NEIGHBOURS)
    #for each auhtor id in the inverted index
    for author in AUTHORS_NEIGHBOURS.keys():
        #for each neighbour id in the list of neighbours
        for neighbour in AUTHORS_NEIGHBOURS[author][0]:
            #add new edge between author and neighbour
            #also computing the weights of each node
            #w(a1, a2) = 1 - J(p1, p2)
            p1 = AUTHORS_NEIGHBOURS[author][1]
            p2 = AUTHORS_NEIGHBOURS[neighbour][1]
            G.add_edge(author, neighbour, weight = 1 - J(p1, p2))  


elapsed_time = time.time() - start_time
print('...Graph creation completed...')
print('Elapsed time: ', elapsed_time)    



###second question
#given a conference in input, return the subgraph induced by the set of authors who
#published at the input conference at least once.

#ask the conference id from the user
conference = int(input ("Insert a conference ID: "))

#for the time computation
start_time = time.time()
#empty list that will contain the id's of the authors matching our requirements
AUTHORS_FOR_SUBGRAPH = []

#for each author in inverted index
for author in AUTHORS_NEIGHBOURS.keys():
    #if the input conference id is one of the conferences of the this author
    if conference in AUTHORS_NEIGHBOURS[author][2]:
        #add this author into the list of authors matching requirements
        AUTHORS_FOR_SUBGRAPH.append(author)

#create the subgraph
SUB_G_1 = G.subgraph(AUTHORS_FOR_SUBGRAPH)

#degree centralitiese computation
DEGREE = nx.degree_centrality(SUB_G_1)
#plot the degree centralities
plt.clf()
plt.figure(figsize=(10,5))
plt.hist(list(DEGREE.values()), bins=30, color='red', histtype='bar')
plt.title('Degree centralities histogram')
plt.xlabel('degree centralities')
plt.ylabel('count')
plt.xlim()
plt.savefig('Degree centralities histogram.png', dpi = 300)
plt.show()
#closeness centralities computation
CLOSENESS = nx.closeness_centrality(SUB_G_1)
#plot the closeness centralities
plt.clf()
plt.figure(figsize=(10,5))
plt.hist(list(CLOSENESS.values()), bins=30, color='blue', histtype='bar')
plt.title('Closeness centralities histogram')
plt.xlabel('closeness centralities')
plt.ylabel('count')
plt.xlim()
plt.savefig('Closeness centralities histogram.png', dpi = 300)
plt.show()
#betweeness centralities computation
BETWEENESS = nx.betweenness_centrality(SUB_G_1)
#plot the betweeness centralities
plt.clf()
plt.figure(figsize=(10,5))
plt.hist(list(BETWEENESS.values()), bins=30, color='green', histtype='bar')
plt.title('Betweeness centralities histogram')
plt.xlabel('betweeness centralities')
plt.ylabel('count')
plt.xlim()
plt.savefig('Betweeness centralities histogram.png', dpi = 300)
plt.show()
                    
elapsed_time = time.time() - start_time
print('...first subgraph creation completed...')
print('Elapsed time: ', elapsed_time)


# given in input an author and an integer d, get the subgraph induced by the nodes that
#have hop distance (i.e., number of edges) at most equal to d with the input author.

#ask the author id from the user
author = int(input ("Insert an author ID: "))
#ask the integer d from the user
d = int(input ("Insert an integer d: "))

#for the time computation
start_time = time.time()

#Calling bfsr wich return a dictionary with nodes matching requirements as keys and hop-distances as values
Hops = bfsi(G, author, d)
    
SUB_G_2 = G.subgraph(list(Hops.keys()))

##Now let's visualise the subgraph

# positions for all nodes
pos=nx.spring_layout(SUB_G_2)
# nodes
nx.draw_networkx_nodes(SUB_G_2, pos, node_size=500)
# edges
nx.draw_networkx_edges(SUB_G_2, pos, edgelist=SUB_G_2.edges(), width=1)
# labels
nx.draw_networkx_labels(SUB_G_2, pos, font_size=5, font_family='sans-serif')

plt.axis('off')
# save as png
plt.savefig("graph-hop distance at most equal to d.png", dpi = 300)
# display
plt.show()

elapsed_time = time.time() - start_time
print('...second subgraph creation completed...')
print('Elapsed time: ', elapsed_time)




###third question
#ask the author id from the user
author = int(input ("Insert an author ID: "))

#for the time computation
start_time = time.time()

#let's find author ID of aris anagnostopoulos
for node in G.node:
    if(G.node[node]['author'] == 'aris anagnostopoulos'):
        ArisID = G.node[node]['author_id']
        break


Shortest_Paths = shortest_path(G, author, ArisID)

elapsed_time = time.time() - start_time
print('...shortest path weight calculation completed...')
print('Elapsed time: ', elapsed_time)

#for the time computation
start_time = time.time()

Shortest_Paths2 = nx.dijkstra_path_length(G, author, ArisID)

elapsed_time = time.time() - start_time
print('...shortest path weight calculation using the networkx function completed...')
print('Elapsed time: ', elapsed_time)

print(Shortest_Paths == Shortest_Paths2)


#Write a Python software that takes in input a subset of nodes (cardinality smaller than
#21) and returns, for each node of the graph, its GroupNumber

I = [int(e) for e in input("Insert a list of author ID's separated by spaces: ").strip().split()]

#for the time computation
start_time = time.time()

GNumbers = GroupNumbers(G, I)

elapsed_time = time.time() - start_time
print('...GroupNumber\'s computation completed...')
print('Elapsed time: ', elapsed_time)