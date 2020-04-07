class Node(object):
	def __init__(self, index):
		self.index = index
		self.edges = []

	def add_edge(self, n, wt, i):
		self.edges.append((i, n, wt))

	def wake_up(self):
		# e = find_min_weight_edge()
		# edges[e].state = BRANCH
		
		# level = 0
		# self.state = FOUND
		# find_count = 0
		# send_message(msg)
		pass