"""
Some Test Scripts
"""

import os
import numpy as np

from test import testing
from scripts import manage

if __name__ == '__main__':
	no_of_random_tests = 1
	max_no_of_nodes = 10
	min_no_of_nodes = 2

	for i in range(no_of_random_tests):
		n = np.random.randint(min_no_of_nodes, max_no_of_nodes)

		testing.big_test(n)
		manage.run_algorithm("inpfile", "outfile")
		
		flag = (testing.check("outfile", "primfile"))
		if not flag:
			print("[*] something is wrong")
			break
		else:
			print("[.] Random test {} - works!".format(i+1))

		os.remove("./inpfile")
		os.remove("./outfile")
		os.remove("./primfile")