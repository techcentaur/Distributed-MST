import sys
from scripts import manage, test

if __name__ == '__main__':

	checkflag = False
	inp = str(sys.argv[1])
	if len(sys.argv)>2:
		out = str(sys.argv[2])
		checkflag = True

	if checkflag:
		ret = test.check(inp, out)
		if ret:
			print("[+] MSTs are same")
		else:
			print("[?] MSTs are different")
	else:
		manage.run_algorithm(inp)