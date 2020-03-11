#ifndef NODE_H
#define NODE_H

#include <iostream>
using namespace std;


enum STATE {SLEEP, FIND, FOUND};
enum STATUS {BASIC, BRANCH, REJECT};

class node{
public:
	node();
	~node();

	// variables
	char name;
	int level; int bestWt; int rec;
	node* parent; node* bestNode; node* testNode;	


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
};

typedef struct edge{
	int a, b, wt;
	edge(int x, int y, int z){
		a = x;
		b = y;
		z = wt;
	}
}edge;

#endif