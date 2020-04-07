class Edge:
	def __init__(self, n1, n2, wt, state="BASIC"):
		# self.s_map = {"BASIC": 0, "BRANCH": 1, "REJECT": 2}

		self.n1 = n1
		self.n2 = n2
		self.wt = wt
		self.state = state

	def __str__(self):
		s = "({}, {}): {} | {}".format(self.n1, self.n2, self.wt, self.state)
		return s