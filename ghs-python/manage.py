import sys
import threading

all_edges = []
all_nodes = []

import node
import edge


if __name__ == '__main__':

	filename = str(sys.argv[1])
	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0])
	all_nodes = []
	for i in range(num_nodes):
		n = node.Node()
		all_nodes.append(n)

	for i in range(len(data)-1):
		n1, n2, wt = data[i+1][1:-1].split(",")
		n1, n2, wt = int(n1), int(n2), int(wt)
		e = edge.Edge(n1, n2, wt)
		all_edges.append(e)
		
		all_nodes[n1].add_edge(i, n2, wt)
		all_nodes[n2].add_edge(i, n1, wt)

	print("[*] No of nodes: {}".format(num_nodes))
	print("[*] No of edges: {}".format(len(data)-1))
