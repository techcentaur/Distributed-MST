import threading



if __name__ == '__main__':
	import sys
	filename = str(sys.argv[1])

	with open(filename, 'r') as f:
		data = (f.read()).splitlines()

	num_nodes = int(data[0])
	edges = []
	for i in range(1, len(data)):
		tmp = data[i][1:-1].split(",")
		edges.append((int(tmp[0]), int(tmp[1]), int(tmp[2])))

	print(num_nodes)
	print(edges)


