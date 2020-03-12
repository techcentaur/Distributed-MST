#ifndef NODE_H
#define NODE_H

#include <iostream>
#include <string>
#include <queue>

using namespace std;

enum STATES {SLEEP, FIND, FOUND};
enum STATUS {BASIC, BRANCH, REJECT};
enum CODE {CONNECT, INITIATE}

class node{
public:
	node();
	~node();

	// variables
	int level;
	string name;
	queue inbox;
	states state;

	int bestWt;
	int rec;
	node* parent;
	node* bestNode;
	node* testNode;

	vector<pair<edge*, node*>> neighbours;

	// functions
	void __init__();
	void receive();
	void initiate();
	void connect();
	void findMin();
	void report();
	void test();
	void accept();
	void reject();
	void changeRoot();

	void addEdge(edge*, node*);
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