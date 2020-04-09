from functools import total_ordering

class Edge:
	def __init__(self, n1, n2, wt):
		self.n1 = n1
		self.n2 = n2
		self.wt = wt

	def __str__(self):
		s = "({}, {}, {})".format(self.n1, self.n2, self.wt)
		return s

@total_ordering
class EdgeNode:
	def __init__(self, index, weight, node, state):
		self.index = index # index of edge in all_edges data structure
		self.weight = weight
		self.node = node
		self.state = state

	def __eq__(self, other):
		return self.weight == other.weight

	def __lt__(self, other):
		return self.weight < other.weight

	def __str__(self):
		s = "{} - {} | *{} | NODE: {}".format(self.index, self.state, self.weight, self.node)
		return s