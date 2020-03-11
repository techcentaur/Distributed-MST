#include <iostream>

using namespace std;

enum STATE {SLEEP, FIND, FOUND};
enum STATUS {BASIC, BRANCH, REJECT};

class node{
public:
	node();
	~node();


	// variables
	char[] name;
	int level, bestWt, rec;
	node* parent, bestNode, testNode;	


	// functions
	void __init__();
	void receive();
	void initiate();
	void findMin();
	void report();
	void test();
	void accept();
	void reject();
	void changeRoot();
}