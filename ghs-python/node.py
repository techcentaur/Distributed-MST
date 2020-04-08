from manange import all_edges, all_nodes
from collections import deque 


class Node(object):
	def __init__(self, index):
		self.index = index
		self.edges = []

		self.state = "SLEEP"
		self.level = -1
		self.find_count = -1

		self.best_edge = -1
		self.best_weight = float('inf')
		self.test_edge = -1

		self.inbox = deque()

	def add_edge(self, i, n, wt):
		self.edges.append((i, n, wt))

	def drop(self, message):
		self.inbox.append(message)

	def online(self):
		while not self.inbox.empty():
			m = self.inbox.popleft()

			if self.state is "SLEEP":
				self.wake_up()

			if m["code"] == "WAKEUP":
				pass
			elif m["code"] == "CONNECT":
				ret = self.connect(m["level"], m["e_index"])
				if not ret:
					self.inbox.append(m)
			elif m["code"] == "INITIATE":
				pass
			elif m["code"] == "TEST":
				pass
			elif m["code"] == "ACCEPT":
				pass
			elif m["code"] == "REJECT":
				pass
			elif m["code"] == "REPORT":
				pass
			elif m["code"] == "CHANGEROOT":
				pass

	def wake_up(self):
		self.edges.sort(key=lambda x: x[2])

		min_edge = self.edges[0]

		all_edges[min_edge].state = "BRANCH"
		self.level = 0
		self.state = "FOUND"
		self.find_count = 0

		message = {
			"code": "CONNECT",
			"level": self.level,
			"e_index": self.edges[min_edge[0]]
		}
		all_nodes[self.edges[min_edge][1]].drop(message)


	def connect(self, level, e_index):
		if self.state is "SLEEP":
			self.wake_up()

		if level < self.level:
			pass
		elif all_edges[e_index].state is "BASIC":
			return False
		else:
			message = {
			"code": "INITIATE",
			"level": self.level+1,
			}
			all_nodes[self.edges[e_index][1]].drop(message)
		return True

 	def initiate(self):
 		


