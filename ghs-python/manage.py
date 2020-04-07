import sys
import threading

from edge import Edge
from node import Node

if __name__ == '__main__':

	filename = str(sys.argv[1])
	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0])
	nodes = []
	for i in range(num_nodes):
		n = Node(i)
		nodes.append(n)

	edges = []
	for i in range(len(data)-1):
		n1, n2, wt = data[i+1][1:-1].split(",")
		n1, n2, wt = int(n1), int(n2), int(wt)
		e = Edge(n1, n2, wt)
		
		edges.append(e)
		nodes[n1].add_edge(n2, wt, i)
		nodes[n2].add_edge(n1, wt, i)

	print("[*] No of nodes: {}".format(num_nodes))
	print("[*] No of edges: {}".format(len(data)-1))
