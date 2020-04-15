import sys
import os

from scripts import manage

if __name__ == '__main__':
	out = None
	inp = str(sys.argv[1])

	if len(sys.argv)>2:
		out = str(sys.argv[2])

	if out is None:
		manage.run_algorithm(inp)
	else:
		manage.run_algorithm(inp, out)