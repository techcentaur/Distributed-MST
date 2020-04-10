from collections import deque 

from . import edge, manage, states

over = False
mst = {}

class Node:
	def __init__(self, i):
		self.S = states.States()
		self.index = i

		self.name = float('inf')
		self.edges = []
		self.lock = None
		self.is_over = False

		self.state = self.S.sleep
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
		self.edges.append(edge.EdgeNode(i, wt, n, self.S.basic))

	def find_min_wt_edge(self):
		__id__ = None
		tmp = edge.EdgeNode(-1, float('inf'), -1, self.S.basic)

		for i in range(len(self.edges)):
			if self.edges[i] < tmp:
				tmp = self.edges[i]
				__id__ = i

		if __id__ is None:
			print("[*] Exception: No min weight edge")
		return __id__

	def convert_indexing(self, wt):
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
				m = self.inbox.popleft()

			if self.state == self.S.sleep:
				self.wake_up()

			i = self.convert_indexing(m["weight"])
			# print("{} <- {} <- {}".format(self.index, m["code"], self.edges[i].node.index))

			if m["code"] == self.S.connect:
				self.connect(m["level"], i)
			elif m["code"] == self.S.initiate:
				self.initiate(m["level"], m["name"], m["state"], i)
			elif m["code"] == self.S.test:
				self.test(m["level"], m["name"], i)
			elif m["code"] == self.S.accept:
				self.accept(i)
			elif m["code"] == self.S.reject:
				self.reject(i)
			elif m["code"] == self.S.report:
				self.process_report(m["best_weight"], i)
			elif m["code"] == self.S.changeroot:
				self.process_change_root()
			else:
				self.wake_up()
		return over

	def wake_up(self):
		# print("WAKE UP | {}".format(self.index))

		min_edge_i = self.find_min_wt_edge()

		with self.lock:
			global mst
			if self.edges[min_edge_i].index not in mst:
				# print("add")
				mst[self.edges[min_edge_i].index] = True

		self.edges[min_edge_i].state = self.S.branch
		self.level = 0
		self.state = self.S.found
		self.rec = 0

		message = {
			"code": self.S.connect,
			"level": 0,
			"weight": self.edges[min_edge_i].weight
		}
		self.edges[min_edge_i].node.drop(message)

	def connect(self, level, i):
		if level < self.level:
			self.edges[i].state = self.S.branch
			message = {
				"code": self.S.initiate,
				"level": self.level,
				"name": self.name,
				"state": self.state,
				"weight": self.edges[i].weight
			}
			self.edges[i].node.drop(message)

			# if self.state == self.S.find:
			# 	self.rec += 1

		elif self.edges[i].state == self.S.basic:
			message = {
				"code": self.S.connect,
				"level": level,
				"weight": self.edges[i].weight
			}
			self.drop(message)
		else:
			message = {
				"code": self.S.initiate,
				"level": self.level+1,
				"name": self.edges[i].weight,
				"state": self.S.find,
				"weight": self.edges[i].weight
			}
			self.edges[i].node.drop(message)

	def initiate(self, level, name, state, i):
		self.level, self.name, self.state = level, name, state
		self.parent = i # as per my indexing

		self.best_node = -1
		self.best_weight = float('inf')

		for e in range(len(self.edges)):
			if (e != i) and (self.edges[e].state == self.S.branch):
				message = {
					"code": self.S.initiate,
					"level": level,
					"name":	name,
					"state": state,
					"weight": self.edges[e].weight
				}
				self.edges[e].node.drop(message)

				# if self.state == self.N.find:
				# 	self.rec +=1

		if state == self.S.find:
			self.rec = 0
			self.find_min()

	def find_min(self):
		idx = -1
		tmp = edge.EdgeNode(-1, float('inf'), -1, self.S.basic)
		for i, e in enumerate(self.edges):
			if e.state == self.S.basic:
				if tmp > e:
					tmp = e
					idx = i

		if idx != -1:
			self.test_node = idx

			message = {
				"code": self.S.test,
				"level": self.level,
				"name": self.name,
				"weight": self.edges[idx].weight
			}
			self.edges[idx].node.drop(message)
		else:
			self.test_node = -1
			self.report()

	def test(self, level, name, i):
		if self.state == self.S.sleep:
			self.wake_up()

		if level > self.level:
			message = {
				"code": self.S.test,
				"level": level,
				"name": name,
				"weight": self.edges[i].weight
			}
			self.drop(message)			

		elif self.name == name:
			if self.edges[i].state == self.S.basic:
				self.edges[i].state = self.S.reject
			if i != self.test_node:
				# drop reject to q (letting him that you've rejected this)
				message = {
					"code": self.S.reject,
					"weight": self.edges[i].weight
				}
				self.edges[i].node.drop(message)
			else:
				self.find_min()
		else:
			# send accept to q
			message = {
				"code": self.S.accept,
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
		if self.edges[i].state == self.S.basic:
			self.edges[i].state = self.S.reject
		self.find_min()	

	def report(self):
		count = 0
		for i in range(len(self.edges)):
			if (self.edges[i].state == self.S.branch) and (i != self.parent):
				count += 1
		if (self.rec == count) and (self.test_node == -1):
			self.state = self.S.found
			message = {
				"code": self.S.report,
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
			if self.state == self.S.find:
				message = {
					"code": self.S.report,
					"best_weight": best_wt,
					"weight": self.edges[i].weight
				}
				self.drop(message)
			elif best_wt > self.best_weight:
				self.change_root()
			elif (best_wt == self.best_weight == float('inf')):
				# print("finish")
				with self.lock:
					global over
					over = True

	def change_root(self):
		if self.edges[self.best_node].state == self.S.branch:
			message = {
				"code": self.S.changeroot,
				"weight": self.edges[self.best_node].weight
			}
			self.edges[self.best_node].node.drop(message)
		else:
			self.edges[self.best_node].state = self.S.branch
			message = {
				"code": self.S.connect,
				"level": self.level,
				"weight": self.edges[self.best_node].weight
			}
			self.edges[self.best_node].node.drop(message)
			
			with self.lock:
				# print("add")
				global mst
				if self.edges[self.best_node].index not in mst:
					mst[self.edges[self.best_node].index] = True


	def process_change_root(self):
		self.change_root()
