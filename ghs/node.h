#ifndef NODE_H
#define NODE_H

#include <iostream>
#include <string>
#include <queue>

using namespace std;

enum STATE {SLEEP, FIND, FOUND};
enum STATUS {BASIC, BRANCH, REJECT};
enum CODE {CONNECT}

class node{
public:
	node();
	~node();

	// variables
	int level;
	string name;
	queue inbox;
	state mystate;

	int bestWt;
	int rec;
	node* parent;
	node* bestNode;
	node* testNode;

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