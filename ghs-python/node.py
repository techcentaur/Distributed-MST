from collections import deque 

from edge import EdgeNode
from manange import all_edges, all_nodes


class Node(object):
	def __init__(self, name):
		self.name = name
		self.edges = []

		self.state = "SLEEP"
		self.level = None
		self.parent = None

		self.inbox = deque()

	def add_edge(self, i, n, wt):
		e = EdgeNode(i, n, wt, "BASIC")
		self.edges.append(e)

	def find_min_wt_edge(self):
		__id__ = 0
		for i in range(1, len(self.edges)):
			if self.edges[i] < self.edges[__id__]:
				__id__ = i
		return __id__

	def get_e_index_from_wt(self, wt):
		for e, i in enumerate(self.edges:)
			if e.weight == wt:
				return i

	def drop(self, message):
		self.inbox.append(message)

	def read(self):
		while not self.inbox.empty():
			__msg__ = self.inbox.popleft()

			if self.state is "SLEEP":
				self.wake_up()

			e_index = get_e_index_from_wt(__msg__["weight"])

			if __msg__["code"] == "WAKEUP":
				pass
			elif __msg__["code"] == "CONNECT":
				ret = self.connect(__msg__["level"], e_index)
				if not ret:
					self.inbox.append(__msg__)
			elif __msg__["code"] == "INITIATE":
				pass
			elif __msg__["code"] == "TEST":
				pass
			elif __msg__["code"] == "ACCEPT":
				pass
			elif __msg__["code"] == "REJECT":
				pass
			elif __msg__["code"] == "REPORT":
				pass
			elif __msg__["code"] == "CHANGEROOT":
				pass

	def wake_up(self):
		min_edge_i = find_min_wt_edge()

		self.edges[min_edge_i].state = "BRANCH"
		
		self.level = 0
		self.state = "FOUND"
		self.find_count = 0

		message = {
			"code": "CONNECT",
			"level": self.level,
			"weight": self.edges[min_edge_i].weight
		}
		all_nodes[self.edges[min_edge_i].node_i].drop(message)


	def connect(self, level, e_index):
		if self.state is "SLEEP":
			self.wake_up()

		if level < self.level:
			self.edges[e_index].state = "BRANCH"
			message = {
				"code": "INITIATE",
				"level": self.level,
				"name": self.name,
				"state": self.state,
				"weight": self.edges[e_index].weight
			}
			all_nodes[self.edges[e_index].node_i].drop(message)

		elif self.edges[e_index].state == "BASIC":
			return False

		else:
			message = {
				"code": "INITIATE",
				"level": self.level+1,
				"name": None, #pq ?
				"state": "FIND",
				"weight": self.edges[e_index].weight
			}
			all_nodes[self.edges[e_index].node_i].drop(message)
		return True

 	def initiate(self, level, name, state, j):
 		self.level, self.name, self.state = level, name, state
 		self.parent = j

 		self.best_edge = None
 		self.best_weight = float('inf')

 		for edge in self.edges:
 			if (edge != j) and (self.edges[edge].state == "BRANCH"):
 				message = {
 					"code": "INITIATE",
 					"level": self.level,
 					"name":	self.name,
 					"state": self.state,
 					"j": None
 				}
 				self.nodes[self.edge[edge].node_index].drop(message)

 		if self.state == "FIND":
 			self.find_count = 0
 			find_min()