"""
I am writing this in python, as this file not asked. //
only for undestanding purposes
"""

import random
import math

class Prim:
	def __init__(self, V, E):
		self.graph = {}
		for i in V:
			self.graph[i] = []

		for i in E:
			self.graph[i[0]].append(i[1])
			self.graph[i[1]].append(i[0])

	def __str__(self):
		return str(self.graph)

	def run(self, v=None):
		self.cost_from_vertex = {}
		self.tree = {}
		self.included = {}

		for k in self.graph:
			self.cost_from_vertex[k] = math.inf
			self.tree[k] = []
			self.included[k] = False

		if v is None:
			v = random.choice(list(self.graph.keys()))
		
		self.cost_from_vertex[v] = 0

		print(self.cost_from_vertex)
		print(self.tree)
		print(self.included)




if __name__ == '__main__':
	v = [x for x in range(10)]
	e = []
	for i in range(15):
		a = random.randint(0, 9)
		b = random.randint(0, 9)
		e.append((a, b))

	p = Prim(v, e)
	p.run()