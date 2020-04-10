def parse(fname):
	with open(fname) as f:
		d = f.read()
	d = d.split("\n")

	l1 = []
	for i in d:
		l1.append(int(i.strip()[1:-1][-1]))
	return l1.sort()

def check(mst1, mst2):
	l1 = parse(mst1)
	l2 = parse(mst2)

	if l1 == l2:
		return True
	return False