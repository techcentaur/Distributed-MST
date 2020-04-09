from collections import deque 

import edge
import manage

class Node:
	def __init__(self, i):
		self.index = i

		self.name = float('inf')
		self.edges = []
		self.lock = None
		self.is_over = False

		self.state = "SLEEP"
		self.parent = None

		self.best_node = -1
		self.test_node = -1
		self.best_weight = float('inf')
		self.rec = -1
		self.level = -1

		self.inbox = deque()

	def __str__(self):
		s = "({}, {})".format(self.index, self.state)
		return s

	def add_edge(self, i, wt, n):
		self.edges.append(edge.EdgeNode(i, wt, n))

	def find_min_wt_edge(self):
		__id__ = None
		tmp = edge.EdgeNode(-1, float('inf'), -1)

		for i in range(len(self.edges)):
			if self.edges[i] < tmp:
				tmp = self.edges[i]
				__id__ = i

		if __id__ is None:
			print("[*] Exception: No min weight edge")
		return __id__

	def get_e_index_from_wt(self, wt):
		for i, e in enumerate(self.edges):
			if e.weight == wt:
				return i

	def __init_lock__(self, lock):
		self.lock = lock

	def drop(self, message):
		with self.lock:
			self.inbox.append(message)

	def read(self):
		if self.inbox:
			with self.lock:
				__msg__ = self.inbox.popleft()

			e_index = self.get_e_index_from_wt(__msg__["weight"])

			if self.state == "SLEEP":
				self.wake_up()

			print("{} <- {} <- {}".format(self.index, __msg__["code"], self.edges[e_index].node.index))
			if e_index == None:
				print("CAN't BE")
				print(__msg__["weight"], __msg__["code"])
				for e in self.edges:
					print(e)

			if __msg__["code"] == "CONNECT":
				self.connect(__msg__["level"], e_index)
			elif __msg__["code"] == "INITIATE":
				self.initiate(__msg__["level"], __msg__["name"], __msg__["state"], e_index)
			elif __msg__["code"] == "TEST":
				self.test(__msg__["level"], __msg__["name"], e_index)
			elif __msg__["code"] == "ACCEPT":
				self.accept(e_index)
			elif __msg__["code"] == "REJECT":
				self.reject(e_index)
			elif __msg__["code"] == "REPORT":
				self.process_report(__msg__["best_weight"], e_index)
			elif __msg__["code"] == "CHANGEROOT":
				self.process_change_root()
			else:
				self.wake_up()

	def wake_up(self):
		print("WAKE UP | {}".format(self.index))

		min_edge_i = self.find_min_wt_edge()

		with self.lock:
			print("ADD MST")
			manage.mst.append(self.edges[min_edge_i].index)

		self.edges[min_edge_i].state = "BRANCH"
		self.level = 0
		self.state = "FOUND"
		self.rec = 0

		message = {
			"code": "CONNECT",
			"level": 0,
			"weight": self.edges[min_edge_i].weight
		}
		self.edges[min_edge_i].node.drop(message)

	def connect(self, level, i):
		if level < self.level:
			self.edges[i].state = "BRANCH"
			message = {
				"code": "INITIATE",
				"level": self.level,
				"name": self.name,
				"state": self.state,
				"weight": self.edges[i].weight
			}
			self.edges[i].node.drop(message)

			# if self.state == "FIND":
			# 	self.rec += 1

		elif self.edges[i].state == "BASIC":
			message = {
				"code": "CONNECT",
				"level": level,
				"weight": self.edges[i].weight
			}
			self.drop(message)
		else:
			message = {
				"code": "INITIATE",
				"level": self.level+1,
				"name": self.edges[i].weight,
				"state": "FIND",
				"weight": self.edges[i].weight
			}
			self.edges[i].node.drop(message)

	def initiate(self, level, name, state, i):
		self.level, self.name, self.state = level, name, state
		self.parent = i # as per my indexing

		self.best_node = -1
		self.best_weight = float('inf')

		for e in range(len(self.edges)):
			if (e != i) and (self.edges[e].state == "BRANCH"):
				message = {
					"code": "INITIATE",
					"level": level,
					"name":	name,
					"state": state,
					"weight": self.edges[e].weight
				}
				self.edges[e].node.drop(message)

				# if self.state == "FIND":
				# 	self.rec +=1

		if self.state == "FIND":
			self.rec = 0
			self.find_min()

	def find_min(self):
		idx = -1
		tmp = edge.EdgeNode(-1, float('inf'), -1)
		for i, e in enumerate(self.edges):
			if e.state == "BASIC":
				if tmp > e:
					tmp = e
					idx = i

		if idx != -1:
			self.test_node = idx

			message = {
				"code": "TEST",
				"level": self.level,
				"name": self.name,
				"weight": self.edges[idx].weight
			}
			self.edges[idx].node.drop(message)
		else:
			self.test_node = -1
			self.report()

	def test(self, level, name, i):
		if self.state == "SLEEP":
			self.wake_up()

		if level > self.level:
			message = {
				"code": "TEST",
				"level": level,
				"name": name,
				"weight": self.edges[i].weight
			}
			self.drop(message)			

		elif self.name == name:
			if self.edges[i].state == "BASIC":
				self.edges[i].state = "REJECT"
			if i != self.test_node:
				# drop reject to q (letting him that you've rejected this)
				message = {
					"code": "REJECT",
					"weight": self.edges[i].weight
				}
				self.edges[i].node.drop(message)
			else:
				self.find_min()
		else:
			# send accept to q
			message = {
				"code": "ACCEPT",
				"weight": self.edges[i].weight
			}
			self.edges[i].node.drop(message)

	def accept(self, i):
		self.test_node = -1
		if self.edges[i].weight < self.best_weight:
			self.best_node = i
			self.best_weight = self.edges[i].weight
		self.report()

	def reject(self, i):
		if self.edges[i].state == "BASIC":
			self.edges[i].state = "REJECT"
		self.find_min()	

	def report(self):
		count = 0
		for i in range(len(self.edges)):
			if (self.edges[i].state == "BRANCH") and (i != self.parent):
				count += 1
		if (self.rec == count) and (self.test_node == -1):
			self.state = "FOUND"
			message = {
				"code": "REPORT",
				"best_weight": self.best_weight,
				"weight": self.edges[self.parent].weight
			}
			self.edges[self.parent].node.drop(message)


	def process_report(self, best_wt, i):
		if self.parent != i:
			# self.rec = self.rec - 1
			if best_wt < self.best_weight:
				self.best_weight = best_wt
				self.best_node = i
			self.rec += 1
			self.report()
		else:
			if self.state == "FIND":
				message = {
					"code": "REPORT",
					"best_weight": best_wt,
					"weight": self.edges[i].weight
				}
				self.drop(message)
			elif best_wt > self.best_weight:
				self.change_root()
			elif (best_wt == self.best_weight == float('inf')):
				self.is_over = True
				print("{} FINIIISH".format(self.index))

	def change_root(self):
		if self.edges[self.best_node].state == "BRANCH":
			message = {
				"code": "CHANGEROOT",
				"weight": self.edges[self.best_node].weight
			}
			self.edges[self.best_node].node.drop(message)
		else:
			self.edges[self.best_node].state = "BRANCH"
			message = {
				"code": "CONNECT",
				"level": self.level,
				"weight": self.edges[self.best_node].weight
			}
			self.edges[self.best_node].node.drop(message)
			
			with self.lock:
				print("ADD MST")
				manage.mst.append(self.edges[self.best_node].index)


	def process_change_root(self):
		self.change_root()