import sys
import threading
import operator

all_edges = []
all_nodes = []
mst = []

import node
import edge

def node_go_brrrrrr(n):
	while not n.is_over:
		n.read()

if __name__ == '__main__':

	filename = str(sys.argv[1])
	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0])
	all_nodes = []
	for i in range(num_nodes):
		n = node.Node(i)
		all_nodes.append(n)

	for i in range(len(data)-1):
		n1, n2, wt = data[i+1][1:-1].split(",")
		n1, n2, wt = int(n1), int(n2), int(wt)
		e = edge.Edge(n1, n2, wt)
		all_edges.append(e)
		
		all_nodes[n1].add_edge(i, wt, all_nodes[n2])
		all_nodes[n2].add_edge(i, wt, all_nodes[n1])

	print("* nodes created")
	threads = []
	for n in all_nodes:
		n.__init_lock__(threading.Lock())
		t = threading.Thread(target=node_go_brrrrrr, args=[n])
		threads.append(t)	
		t.start()

	print("all threads started")
	all_nodes[0].wake_up()
	for t in threads:
		t.join()

	print("*we done here")


	# print("[*] No of nodes: {}".format(num_nodes))
	# print("[*] No of edges: {}".format(len(data)-1))

	mst_edges = [all_edges[i] for i in mst]
	mst_edges.sort(key=operator.attrgetter('wt'))

	for m in mst_edges:
		print(mst_edges)