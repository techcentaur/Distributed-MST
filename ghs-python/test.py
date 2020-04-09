import sys

def parse(fname):
	with open(fname) as f:
		d = f.read()
	d = d.split("\n")

	l1 = []
	for i in d:
		l1.append(int(i[1:-1][-1]))

	return l1.sort()

l1 = parse(str(sys.argv[1]))
l2 = parse(str(sys.argv[2]))

if l1 == l2:
	print("Same")
else:
	print("Not Same")