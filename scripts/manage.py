import sys
import threading
import operator

all_edges = []
all_nodes = []
mst = {}

from . import node, edge

def node_go_brrrrrr(n):
	while True:
		ret = n.read()
		if ret:
			return

def run_algorithm(filename):
	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0])
	all_nodes = []
	for i in range(num_nodes):
		n = node.Node(i)
		all_nodes.append(n)

	for i in range(len(data)-1):
		n1, n2, wt = (data[i+1].strip())[1:-1].split(",")
		n1, n2, wt = int(n1), int(n2), int(wt)
		e = edge.Edge(n1, n2, wt)
		all_edges.append(e)
		
		all_nodes[n1].add_edge(i, wt, all_nodes[n2])
		all_nodes[n2].add_edge(i, wt, all_nodes[n1])

	threads = []
	for n in all_nodes:
		n.__init_lock__(threading.Lock())
		t = threading.Thread(target=node_go_brrrrrr, args=[n])
		threads.append(t)	
		t.start()

	all_nodes[0].wake_up()
	for t in threads:
		t.join()

	# print("[*] No of nodes: {}".format(num_nodes))
	# print("[*] No of edges: {}".format(len(data)-1))

	mst_edges = [all_edges[k] for k, v in node.mst.items()]
	mst_edges.sort(key=operator.attrgetter('wt'))

	for m in mst_edges[:-1]:
		print(m)
	print(mst_edges[-1], end='')