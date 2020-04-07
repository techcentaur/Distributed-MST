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
			message = self.inbox.popleft()

			if self.state is "SLEEP":
				self.wake_up()

			if message["code"] == "INITIATE":
				pass
			elif message["code"] == "CONNECT":
				pass
			elif message["code"] == "INITIATE":
				pass
			elif message["code"] == "TEST":
				pass
			elif message["code"] == "ACCEPT":
				pass
			elif message["code"] == "REJECT":
				pass
			elif message["code"] == "REPORT":
				pass
			elif message["code"] == "CHANGEROOT":
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
		}
		all_nodes[self.edges[min_edge][1]].drop(message)

