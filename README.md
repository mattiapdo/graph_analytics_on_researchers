# ADM-HW4

###Excercise 1


we want to build two dictionaries:

    AUTHORS_TO_INSERT = {author_id_1: authordict1, author_id_2:...}
    AUTHORS_NEIGHBOURS = {author_id_1: [[neighbour_id_1, neighbour_id_2, neighbour_id_3,...], [publication_id_1, publication_id_2,...], [conference_id_1, conference_id_2,...]], author_id_2 : ...}

The inverted index AUTHORS_NEIGHBOURS is going to be used during the creation of edges and also during the looking out of authors who published in a given conference at least once.

Taking the data from the json file:
    
    for each conference in the json file

      for each author in that conference
      
              if the author is not yet in the list of authors to insert
                  insert it into the list of authors to insert
                  
              if author already in the inverted index
                  update the value with key author in the inverted index
                  here we add all the authors in the actual conference into the 
                  list of neighbours removing duplicates
                  We also add the current publication in the list of publications
                  and the current conference in the list of conferences
                  
              if the author not already in inverted index
                  add author in inverted index setting the dictionary of
                  neighbours to all the authors in the actual conference
                  removing duplicates,
                  setting the list of publications to the actual publication
                  and the list of conferences to the actual conference

Building the graph:
    
    here we use the first dictionary (AUTHORS_TO_INSERT) 
    to add nodes to the graph: we add as node value the author_id and as attribut the author_name
    
    we use the second dictionary (the inverted index AUTHORS_NEIGHBOURS) to add edges:
    
    for each author_id in AUTHORS_NEIGHBOURS    
        for each neighbour id in the list of neighbours
            add new edge between author_id and neighbour
            also computing the weight of each node:
              w(a1, a2) = 1 - J(p1, p2)
    	     where p1 and p2 are the sets of publications 
    	     respectively of the author and the neighbour
    	     and the set of publications here are still taken from the inverted index
    	     The function J() which computes the jaccard similarity is written in the file
    	     Libhw4.py

          
###Excercise 2.a

Given a conference in input, return the subgraph induced by the set of authors who published at the input conference at least once.

- ask the conference id from the user, for example 3345
- create an empty list that will contain the id's of the authors matching our requirements (AUTHORS_FOR_SUBGRAPH)

.

    for each author in inverted index (AUTHORS_NEIGHBOURS)
        if the input conference id is one of the conferences of the this author
            add this author into the list of authors matching requirements
	
- create the subgraph using the list of authors matching requirements

Do some statistics
    
    degree centralities computation
    DEGREE = nx.degree_centrality(SUB_G_1)
    plot the degree centralities
    
    closeness centralities computation
    CLOSENESS = nx.closeness_centrality(SUB_G_1)
    plot the closeness centralities
    
    betweeness centralities computation
    BETWEENESS = nx.betweenness_centrality(SUB_G_1)
    plot the betweeness centralities        


###Excercise 2.b


Given in input an author and an integer d, get the subgraph induced by the nodes that have hop distance (i.e., number of edges) at most equal to d with the input author.

- ask the author id from the user, for example 256176
- ask the integer d from the user, for example 2

we have implemented two functions:

#### 2.b.1)  iterative version	

    bfsi(G, source, d = 0, OUTPUT = {}, TO_VISIT = deque([]))

It is a function that implements the breath first traversal and construct a dictionary with all nodes as keys and the number of hop from source to the node as values. the function do not visit a node not matching the requirement of hop_distance < d and return the resulting dictionary.


(a) it returns a dictionary of nodes already visited (OUTPUT)

  - key = node
  
  - value = number of hops to get there from the source

(b) we make use of a FIFO queue of nodes to visit (TO_VISIT)

.

    starting from the source node..
    if no neighbor or all neighbors already visited
          	pass
    else
    	for each neighbour among the source neighbours
          add them into the queue and into the visited nodes(OUTPUT)
    	    if the neighbour is not in the dictionary
    	       insert in the queue a tuple, containing :
    	       neighbour and hop_distance = 1
             store in the OUTPUT dictionary the neighbour_id as key and the 
             hop_distance = 1 from the source as value
                   
    while there is something to visit
          remove the first element from the queue in order to visit it (FIFO)
                    
    	    if the node we are going to visit has a hop_distance <= d then we visit it
    
              if no neighbor for this node, or all neighbors already visited
                  pass
              else
                  for neighbor in all neighbors of this node
                      if the neighbor has not been visited yet
                          add it into the  queue 
                          and store it in the OUTPUT dictionary, with neighbor_id as key and hop_distance of the
                          node we are visiting incremented by one
                        
                        
    then we are done visiting everything so we can return the output dictionary
    return the dictionary (OUTPUT)
    
    
#### 2.b.2)  recursive version


    bfsr(G, source, d, OUTPUT = {}, TO_VISIT = deque([]), hop = 0, flag = 1)

This function as the previous implements the breath first traversal and construct a dictionary with all nodes as keys and the number of hop from source to the node as values. the function do not visit a node not matching the requirement of hop_distance < d and return the resulting dictionary.

(a) it returns a dictionary of nodes already visited (OUTPUT)
  
  - key = node
  - value = number of hops to get there from the source

(b) we make use of a FIFO queue of nodes to visit (TO_VISIT)

.

    if we are at the first iteration 
    (we make use of a flag variable to check it with flag = 1)
       add the source to the dictionary with 0 as number of hops
       and set the flag variable to 0
        
    if no neighbor or all neighbors already visited
       return the dictionary (OUTPUT)

    for each neighbour of the source
       if it has not already been visited
       	  add if into the queue and
       	  add it into the OUTPUT dictionary 
       	  (key = neighbour, value = hop distance of source(which is 0) +1)
        
    while there is something to visit
        remove the first element from the queue in order to visit it (FIFO)
       
        if the node we are going to visit has a hop_distance <= d then we visit it
          call the fuction (recursively): 
          bfsr(G, source = node[0], radius = d, OUTPUT, TO_VISIT, hop= node[1], flag = 0),
    	   
    	   passing as parameters
    	   - the node where we are as 'source'
    	   - hop: hop distance of the current node
    	   - flag = 0 because we will not be in the first iteration anymore
    
    we are done visiting everything so we can return the output dictionary
    return OUTPUT


#### module Libhw4.py

In this module, we implemented 4 main functions which are bfsr(), bfsi(), shortest_path() and GroupNumbers().
the two bfs functions have already been explain previously.


now let's explain the shortest_path() function:

the goal of this function is to compute the shortest path weight from a source to a destination node,
this function is just an addaptation of the bfsi function used above.

The logic:

(a) it creates a dictionary of nodes already visited (OUTPUT)
  
  - key = node
  - value = number of hops to get there from the source

(b) we make use of a FIFO queue of nodes to visit (TO_VISIT)

.

    if no neighbor
        pass
    else
        for each neighbor in all neighbors of the source
            add them into the To_VISIT queue as a set
            (neighbour, weight of the edge between source and the neighbor)
            add them into the OUTPUT dictionary
            (key = neighbour, value = weight of the edge between source and the neighbor)
    
    while there is something to visit
        remove the first element from the queue in order to visit it (FIFO)
        
        if no neighbor
            pass
        else
            for neighbor in all neighbors of the actual node
                if the neighbor is not visited yet 
                    add it into the to visited queue as a set
                    (neighbour, weight of the edge between source and the neighbor)
                    and into the OUTPUT dictionary
                    (key = neighbour, value = weight of the actual node + weight of the edge between actual node and the neighbor)
                
                if the neighbor is yet visited
                    check if the actual weight is less than the old one and replace if it does
    
    we are done visiting everything so we can return the shortest path weight for the source
    if destination is in the OUTPUT dictionary
        return OUTPUT[destination]
    else
        return None


now let's explain the GroupNumbers() function:

the goal here is to return a dictionary containing all the nodes of the graph as keys and the lowest shortest path from u to the other nodes of the graph as values, for each u in nodes_set.

this function just compute for each value in the input nodes_set the shortest path from them to all the other nodes in the graph.
in this way every time the values that are greter in the OUTPUT dictionary are going to be overwrite by the ones that are lower.

Exemple:
graph_nodes = [a, b, c, d, e]
nodes_set = [a, b, c]
shortest path from a to all other nodes:
OUTPUT = {a: 0, b: 2, c:1, d:5, e:6}
shortest path from b to all other nodes:
here we check d(b, a) < OUTPUT[a]? No then we do nothing
otherwise we update OUTPUT[a].

