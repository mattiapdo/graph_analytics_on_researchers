#%%
'''...importing some usefull library...'''
import time
import json
import networkx as nx
import matplotlib.pyplot as plt
import Libhw4 as lb
import pprint as pp


start_time = time.time()    
'''...The code...''' 
###first question

#creation of an empty graph G
G = nx.Graph()
G.Name = 'Authors'

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
with open('full_dblp.json') as json_data:
    data = json.load(json_data)
    # for each publication in the json file
    for publication in data:
        #for each author in the current publication,
        for author in publication['authors']:
            #if author not already inserted in the graph
            if author['author_id'] not in AUTHORS_NEIGHBOURS.keys():
                #create an empty field for the current author in the inverted index
                AUTHORS_NEIGHBOURS[author['author_id']] = [set([]),set([]),set([])]
                #add a node in the graph storing the author_id as node and the author name as attribute
                G.add_node(author['author_id'], author = author['author'])
                                
                #let's modify the set of neighbors, publications and conferences for this author
                neighbours = set([publication['authors'][i]['author_id'] for i in range(len(publication['authors']))])
                publications = set([publication['id_publication_int']]) 
                conferences = set([publication['id_conference_int']])
                
                #update values in the inverted index
                AUTHORS_NEIGHBOURS[author['author_id']][0] = AUTHORS_NEIGHBOURS[author['author_id']][0].union(neighbours)
                AUTHORS_NEIGHBOURS[author['author_id']][1] = AUTHORS_NEIGHBOURS[author['author_id']][1].union(publications)
                AUTHORS_NEIGHBOURS[author['author_id']][2] = AUTHORS_NEIGHBOURS[author['author_id']][2].union(conferences)
                
                #for each neighbor of the current author,
                for neighbour in neighbours :
                    #if the authors aren't connected yet,
                    if not lb.nodes_connected(G, author['author_id'], neighbour) and author['author_id'] != neighbour:
                        #then connect them
                        G.add_edge(author['author_id'], neighbour)
            
            #if the author is already in the graph,
            else:
                #let's modify the set of neighbors, publications and conferences for this author
                neighbours = set([publication['authors'][i]['author_id'] for i in range(len(publication['authors']))])
                publications = set([publication['id_publication_int']])     
                conferences = set([publication['id_conference_int']])
                
                #update values in the inverted index
                AUTHORS_NEIGHBOURS[author['author_id']][0] = AUTHORS_NEIGHBOURS[author['author_id']][0].union(neighbours)
                AUTHORS_NEIGHBOURS[author['author_id']][1] = AUTHORS_NEIGHBOURS[author['author_id']][1].union(publications)
                AUTHORS_NEIGHBOURS[author['author_id']][2] = AUTHORS_NEIGHBOURS[author['author_id']][2].union(conferences)
                  
                #for each neighbor of the current author,
                for neighbour in neighbours :
                    #if the authors aren't connected yet,
                    if not lb.nodes_connected(G, author['author_id'], neighbour) and author['author_id'] != neighbour:
                        #then connect them
                        G.add_edge(author['author_id'], neighbour)
                
                
            


elapsed_time = time.time() - start_time
print('\n...data loaded...\n...graph creation completed...')
print('Elapsed time: ', elapsed_time)    
print('\n',nx.info(G))


start_time= time.time()

#for each author (already inserted in the graph)
for author in AUTHORS_NEIGHBOURS.keys():
    #for each neighbor of the current author (from the inverted index)
    for neighbour in AUTHORS_NEIGHBOURS[author][0]:
        #if they are connected,
        if lb.nodes_connected(G, author, neighbour):
            #compute the weight of the edge
            #between author and neighbour
            #w(a1, a2) = 1 - J(p1, p2) 
            G[author][neighbour]['weight'] = 1 - lb.J(AUTHORS_NEIGHBOURS[author][1], AUTHORS_NEIGHBOURS[neighbour][1])
            
elapsed_time = time.time() - start_time
print('\n...weights computation completed...')
print('Elapsed time: ', elapsed_time)

#%%

###second question
#given a conference in input, return the subgraph induced by the set of authors who
#published at the input conference at least once.
print('\n****************************************************************************\n',
      'Given a conference in input, the program returns the subgraph induced\n',
      'by the set of authors who published at the input conference at least once',
      '\n****************************************************************************\n')
#ask the conference id from the user, for example 3345
conference = int(input ("Insert the conference ID: "))

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

elapsed_time = time.time() - start_time
print('\n...first subgraph creation completed...')
print('Elapsed time: ', elapsed_time)
#%%
print('\n**************************\n',
      'Here are some statistics',
      '\n**************************\n')
start_time = time.time()
#degree centralities computation
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
plt.title('Betweenness centralities histogram')
plt.xlabel('betweenness centralities')
plt.ylabel('count')
plt.xlim()
plt.savefig('Betweenness centralities histogram.png', dpi = 300)
plt.show()
                    
elapsed_time = time.time() - start_time
print('...centrality measures computation done...\n...histograms creation done...')
print('Elapsed time: ', elapsed_time)
#%%
print('\n****************************************************************************\n',
      'Given in input an author and an integer d the program returns the subgraph\n', 
      'induced by the nodes that have hop distance at most equal to d', 
      '\n****************************************************************************\n')
# given in input an author and an integer d, get the subgraph induced by the nodes that
#have hop distance (i.e., number of edges) at most equal to d with the input author.
#ask the author id from the user, for example 256176
author = int(input ("Insert an author ID: "))
#ask the integer d from the user, for example 5
d = int(input ("Insert an integer d: "))

print('\nChoose what function you wish to use in order to compare the computation times'
      '\n1 for iterative breath first search algorithm',
      '\n2 for recursive breath first search algorithm',
      '\n3 for networkx.ego_graph()\n'
      '  essentially based on single source Dijkstra',
      '\ne to exit\n')
choice = input()
while choice != 'e':
    if choice == '1': 
        #for the time computation
        start_time = time.time()
        #Calling bfsr wich return a dictionary with nodes matching requirements as keys and hop-distances as values
        Hops = lb.bfsi(G, author, d)
        #create the subgraph
        SUB_G_2 = G.subgraph(list(Hops.keys()))
        elapsed_time = time.time() - start_time
        print('\n...subgraph creation completed...\nElapsed time: ', elapsed_time)
    elif choice == '2': 
        #for the time computation
        start_time = time.time()
        #Calling bfsr wich return a dictionary with nodes matching requirements as keys and hop-distances as values
        Hops = lb.bfsr(G, author, d)
        #create the subgraph
        SUB_G_2 = G.subgraph(list(Hops.keys()))
        elapsed_time = time.time() - start_time
        print('\n...subgraph creation completed...\nElapsed time: ', elapsed_time)
    elif choice == '3': 
        #for the time computation
        start_time = time.time()
        #create the subgraph
        SUB_G_2 = nx.ego_graph(G, author, radius=d)
        elapsed_time = time.time() - start_time
        print('\n...subgraph creation completed...\nElapsed time: ', elapsed_time)
    else: print('\nError: insert a valid choice\n')
        
    print('\nChoose what function you wish to use in order to compare the computation times'
      '\n1 for iterative breath first search algorithm',
      '\n2 for recursive breath first search algorithm',
      '\n3 for networkx.ego_graph()\n'
      '  essentially based on single source Dijkstra\n',
      'e to exit\n')
    choice = input()

print('\n**********************************\n',
      "Now let's visualise the subgraph", 
      '\n**********************************\n')

print('\n...plotting the graph...\n')
start_time = time.time()
# positions for all nodes
pos=nx.spring_layout(SUB_G_2)
# nodes
nx.draw_networkx_nodes(SUB_G_2, pos, node_size=10, node_color ='red', alpha = 0.5)
# edges
nx.draw_networkx_edges(SUB_G_2, pos, edgelist=SUB_G_2.edges(), width=1, edge_color = 'yellow')
# labels
nx.draw_networkx_labels(SUB_G_2, pos, font_size=1, font_family='sans-serif')
plt.axis('off')
# save as png
plt.savefig("graph-hop distance at most equal to d.png", dpi = 300)
# display
plt.show()

elapsed_time = time.time() - start_time
print('Elapsed time: ', elapsed_time)

#%%
print('\n***************************************************************************\n',
      'takes in input an author (id) and returns the weight of the shortest path\n',
      'that connects the input author with Aris.', 
      '\n***************************************************************************\n')

###third question
#ask the author id from the user, for example 17528
author = int(input ("Insert the author ID: "))
#for the time computation


#let's find author ID of Aris Anagnostopoulos
for node in G.node:
    if(G.node[node]['author'] == 'aris anagnostopoulos'):
        ArisID = node
        break

print('\nChoose what function you wish to use in order to compare the computation times',
          '\n1 for Libhw4.shortest_path()',
          '\n2 for nx.dijkstra_path_length()',
          '\ne to exit')
choice = input()
while choice != 'e':
    if choice == '1':  
        start_time = time.time()
        Shortest_Paths = lb.shortest_path(G, author, ArisID)
        print('\nShortest path between Aris and', author, 'is',
              Shortest_Paths,'\n')
        elapsed_time = time.time() - start_time
        print('\n...shortest path weight calculation completed...')
        print('\tElapsed time: ', elapsed_time)

    elif choice == '2': 
        start_time = time.time()
        Shortest_Paths = nx.dijkstra_path_length(G, author, ArisID)
        print('\nShortest path between Aris and', author, 'is',
              Shortest_Paths,'\n')
        elapsed_time = time.time() - start_time
        print('\n...shortest path weight calculation using the networkx function completed...')
        print('\tElapsed time: ', elapsed_time)

    else: print('\nError: insert a valid choice')

    print('Choose what function you wish to use in order to compare the computation times',
          '\n1 for Libhw4.shortest_path()',
          '\n2 for nx.dijkstra_path_length()',
          '\ne to exit')
    choice = input()
#%%
#Write a Python software that takes in input a subset of nodes (cardinality smaller than
#21) and returns, for each node of the graph, its GroupNumber
print('\n********************************************\n',
      'Take in input a subset of nodes and return',
      '\nfor each node of the graph, its GroupNumber', 
      '\n********************************************\n')
#input some node.. for example 365066 273515 17528 19210 364934
I = [int(e) for e in input("Insert a list of author ID's separated by spaces\nmax 21 items: ").strip().split()]
while len(I) >21:
    I = [int(e) for e in input("Insert a list of author ID's separated by spaces\nmax 21 items: ").strip().split()]

#for the time computation
start_time = time.time()

GNumbers = lb.GroupNumbers(G, I)

pp.pprint(GNumbers)
print('Author: (Min Shortest Path, Best Input Node)\n')
elapsed_time = time.time() - start_time
print('...GroupNumber\'s computation completed...')
print('Elapsed time: ', elapsed_time)
