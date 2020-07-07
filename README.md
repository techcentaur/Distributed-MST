# Distributed MST
Implementing Distributed Minimum Spanning Tree With the Help of GHS Distributed algorithm

Can be  applied in topological observability in power systems; management of indepedent systems sounds like the apt way, but I'm just guessing theoretically.

Wiki for GHS - [link](https://en.wikipedia.org/wiki/Distributed_minimum_spanning_tree)

## Pre-conditions of Network
– Messages can be transmitted independently in both directions on Edge ("transfer" mode) and arrive without error (after a finite delay.): Fair assumption; can be managed in any pragammatic situation.
– Each edge delivers messages in FIFO order: Achieved with a Queue.
– The graph must be connected and undirected: Since it's a simulation, "connection" is easy, but in a real-action one might need some rule to manage the assumed  inter-connection.
– The graph should have distinct finite edge-weights (or some consistent way to
remove ties.): This maybe weird but since needed by the algorithm can be managed in a "proxy" way; say by creating a unique "edge-weight", e.g., "?weight#node1#node2".


## Construction of Node

Think of Node as an entity that has the knowledge of means of transfer to it (here Edge).

So, each Node knows the "weight" for each Edge incident to that Node. In this algorithm, we assume each Node to be in a "sleep" state initially (and it either spontaneously self-awakens or is awakened by receiving any message from another node); this is an assumption and can be manipulated as per the need of the application of the algorithm.

Yes, the Node will manage an inbox system for asyn message passing. Any `		self.inbox = deque()` would work. And yes, then the Node will check its messages in a loop. Something like this would be fairly easy to understand.

```python
	def read(self):
		if self.inbox:
			ret = 0
			with self.lock:
				m = self.inbox.popleft()

			if m["code"] == "wake":
				self.wake_up()
				return False

			if self.state == self.S.sleep:
				self.wake_up()

			i = self.convert_indexing(m["weight"])
			if m["code"] == self.S.connect:
				ret = self.connect(m["level"], i)
			elif m["code"] == self.S.initiate:
				self.initiate(m["level"], m["name"], m["state"], i)
			elif m["code"] == self.S.test:
				ret = self.test(m["level"], m["name"], i)
			elif m["code"] == self.S.accept:
				self.accept(i)
			elif m["code"] == self.S.reject:
				self.reject(i)
			elif m["code"] == self.S.report:
				ret = self.process_report(m["best_weight"], i)
			elif m["code"] == self.S.changeroot:
				self.process_change_root()
			elif m["wake"] == "wake":
				self.wake_up()

			if ret == -1:
				self.drop(m)
		return over
```

The else-if conditions are dependent on the possible states of Node or Edge. I wouldn't go any deeper, rest functions are easy-written; take a look [here](./scripts/node.py).

## Construction of Edge

We only need an object that encapsulates traits of Edge, that's all. Something like this would do.

```python
class EdgeNode:
	def __init__(self, index, weight, node, state):
		self.index = index # index of edge in all_edges data structure
		self.weight = weight
		self.node = node
		self.state = state

```

Edge code [here](./scripts/edge.py)

## Managing Algorithm

- Create one thread per Node.
- Run it in a loop for checking inbox of a message.
- Wake the first node up.
- When all threads are finished, reterive the globally agreed MST.


## References:
[Link for the enhanced research paper by GHS](./papers/GHS_enhanced.pdf)