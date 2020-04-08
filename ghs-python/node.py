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
				if ret == -1:
					self.drop(__msg__)
			elif __msg__["code"] == "INITIATE":
				self.initiate(__msg__["level"], __msg__["name"], __msg__["state"], e_index)
			elif __msg__["code"] == "TEST":
				ret = self.test(__msg__["level"], __msg__["name"], e_index)
				if ret == -1:
					self.drop(__msg__)
			elif __msg__["code"] == "ACCEPT":
				self.accept(e_index)
			elif __msg__["code"] == "REJECT":
				self.reject(e_index)
			elif __msg__["code"] == "REPORT":
				self.process_report(__msg__["best_weight"], e_index)
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
			return -1

		else:
			message = {
				"code": "INITIATE",
				"level": self.level+1,
				"name": None, #pq ?
				"state": "FIND",
				"weight": self.edges[e_index].weight
			}
			all_nodes[self.edges[e_index].node_i].drop(message)
		return 1

 	def initiate(self, level, name, state, j):
 		self.level, self.name, self.state = level, name, state
 		self.parent = j # according of my indexing

 		self.best_node = None
 		self.best_weight = float('inf')
 		self.test_node = None

 		for e in range(len(self.edges)):
 			if (e != j) and (self.edges[e].state == "BRANCH"):
 				message = {
 					"code": "INITIATE",
 					"level": self.level,
 					"name":	self.name,
 					"state": self.state,
 					"weight": self.edges[e].weight
 				}
 				self.nodes[self.edges[e].node_i].drop(message)

 		if self.state == "FIND":
 			self.find_count = 0
 			find_min()

 	def find_min(self):
 		idx = -1
 		tmp = EdgeNode(-1, float('inf'), -1)
 		for e in self.edges:
 			if self.edges[e].state == "BASIC":
 				if tmp > self.edges[e]:
 					idx = e

 		if idx != -1:
 			self.test_node = None
 			message = {
 				"code": "TEST",
 				"level": self.level,
 				"name": self.name,
 				"weight": self.edges[idx].weight
 			}
 			all_nodes[self.edges[idx].node_i].drop(message)
 		else:
 			self.test_node = None
 			report()

 	def test(self, level, name, i):
 		if self.level < level:
 			return -1
 		elif self.name == name:
 			if self.edges[i].state == "BASIC":
 				self.edges[i].state == "REJECT"
 			if i != self.test_node:
 				# drop reject to q (letting him that you've rejected this)
 				message = {
 					"code": "REJECT",
 					"weight": self.edges[i].weight
 				}
 				all_nodes[self.edges[i].node].drop(message)
 			else:
 				find_min()
 		else:
 			# send accept to q
 			message = {
 				"code": "ACCEPT",
 				"weight": self.edges[i].weight
 			}
 			all_nodes[self.edges[i].node].drop(message)
 		return 1

 	def accept(self, i):
 		self.test_node = None
 		if self.edges[i].weight < self.best_weight:
 			self.best_node = i
 			self.best_weight = self.edges[i].weight
 		report()

 	def reject(self, i):
 		if self.edges[i].state == "BASIC":
 			self.edges[i].state == "REJECT"
 		find_min()	

 	def report(self):
 		count = 0
 		for i in range(len(self.edges)):
 			if (self.edges[i].state == "BRANCH") and (i != self.parent):
 				count+=1
 		if (self.find_count == count) and (self.test_node == None):
 			self.state = "FOUND"
 			message = {
 				"code": "REPORT",
 				"weight": self.edges[self.parent].weight
 				"best_weight": self.best_weight
 			}
 			all_nodes[self.edges[self.parent].node_i].drop(message)


 	def process_report(self, best_wt, i):
 		if self.parent != i:
 			if best_wt < self.best_weight:
 				self.best_weight = best_wt
 				self.best_node = i
 			self.rec += 1
 			report()
 		else:
 			if self.state == "FIND":
 				return -1
 			elif best_wt > self.best_weight:
 				change_root()
 			elif (best_wt == self.best_weight) and (self.best_weight == float('inf')):
 				# stop

 	def change_root(self):
 		pass

 	def process_change_root(self):
 		self.change_root()