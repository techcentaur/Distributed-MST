import sys
import os
import numpy as np

from . import prims

def big_test(n):
	a = np.random.choice(np.arange(0, 2*n*n), replace=False, size=(n, n))

	for i in range(n):
		a[i][i] = 0

	a = np.maximum( a, a.transpose() )

	dfile = "inpfile"
	dfile2 = "primfile"

	prims.prims(n, a, dfile2)

	data = "{}\n".format(n)
	for i in range(n):
		for j in range(i+1, n):
			if a[i][j]:
				data += "({}, {}, {})\n".format(i, j, a[i][j])
	data = data[:-1]

	with open(dfile, 'w') as f:
		f.write(data)

	return dfile

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
