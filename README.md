# GHS-distributed
Implementing GHS distributed algorithm


Here's how I am going to start:

1. Writing Prim's algorithm
2. Writing structure and psuedocode for all files, classes, methods and all that is required 
// as per in the slides
3. Then I think about making is distributed
4. Write the code piece by piece and keep on testing


- A node will have inbox so any node can put any type of packet in it, and when a thread will access the node it will check its inbox, pop a message and check what to do - this is the control flow movement
- I think a node only knows its neighbours, because he'd send only those packets to them and can check only those corresponding edges and nothing more.
- But then how would I give a node a particular number of edges? It must be when a node is initialised right? That seems the right way.

- init node
- tell him its neigh and edges
- it will send a message by dropping a message in its inbox (this can be done without locking as lock would be in the queue itself)
- but then what happen when it needs to change state of edge?
- can another node at the same time change it?
- might need to put a lock there.
- i probably will go this implementation - will think about the lock later.