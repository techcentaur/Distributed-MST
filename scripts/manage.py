import sys
import threading
import operator

all_edges = []
all_nodes = []

from . import node, edge

mst = {}
def node_go_brrrrrr(n):
	while True:
		ret = n.read()
		if ret:
			with n.lock:
				global mst
				for k, v in n.mst.items():
					if k not in mst:
						mst[k] = True
			return

def run_algorithm(filename, out=None):
	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0].strip())
	if num_nodes == 1:
		if out is None:
			return
		else:
			with open(out, 'w') as f:
				f.write("")


	for i in range(num_nodes):
		n = node.Node(i)
		all_nodes.append(n)
		n.__init_lock__(threading.Lock())


	for i in range(len(data)-1):
		n1, n2, wt = (data[i+1].strip())[1:-1].split(",")
		n1, n2, wt = int(n1), int(n2), int(wt)
		all_edges.append(edge.Edge(n1, n2, wt))
		
		all_nodes[n1].add_edge(i, wt, all_nodes[n2])
		all_nodes[n2].add_edge(i, wt, all_nodes[n1])


	# threads = []
	# all_nodes[0].wake_up()
	# while True:
	# 	for n in all_nodes:
	# 		ret = n.read()
	# 		if ret:
	# 			break
	# 	else:
	# 		continue
	# 	for n in all_nodes:
	# 		for k, v in n.mst.items():
	# 			if k not in mst:
	# 				mst[k] = True
	# 	break

	threads = []
	for i, n in enumerate(all_nodes):
		t = threading.Thread(target=node_go_brrrrrr, args=[n])
		threads.append(t)	
		t.start()

	all_nodes[0].wake_up()
	for t in threads:
		t.join()

	mst_edges = [all_edges[k] for k, v in mst.items()]
	mst_edges.sort(key=operator.attrgetter('wt'))

	if out is None:
		for m in mst_edges[:-1]:
			print(m)
		print(mst_edges[-1], end='')
	else:
		s = ""
		for m in mst_edges[:-1]:
			s += m.__str__() + " \n"
		s += mst_edges[-1].__str__() + " "

		with open(out, 'w') as f:
			f.write(s)
