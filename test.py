import os
import numpy as np

from test import testing
from scripts import manage

if __name__ == '__main__':
	no_of_random_tests = 100
	max_no_of_nodes = 100
	min_no_of_nodes = 2

	for i in range(no_of_random_tests):
		n = np.random.randint(min_no_of_nodes, max_no_of_nodes)

		testing.big_test(n)

		### change this line // call your algorithm
		#
		# this should write all MST edges in a file named
		# "outfile" in sorted order of weights (asc)
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