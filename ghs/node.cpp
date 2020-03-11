#include "node.h"
#include <iostream>
#include <queue>
#include <limits>

using namespace std;

node::node(){
	mystate = SLEEP;
}

node::~node(){}

node::__init__(){
	this->mystate = FOUND;
	this->level = 0;
	this->rec = 0;
	
	packet p = new Packet(CONNECT, 0);
	this->send(&p); // to q
}

node::receive(){
	packet* p = this->queue.front();
	if (p->code == CONNECT){
		this->connect(p);
	}
	else if(p->code == INITIATE){
		this->initiate(p);
	}


	this->queue.pop();
}

node::connect(packet* p){
	if (p->level < this->level){
		// combine with rule LT
		// edge from p-q status <- branch
		packet p = new Packet(INITIATE, this->level,
							this->name, this->mystate);
		this->send(&p); // to q
	}
	else if(status[q] == BASIC){
		wait();
	}
	else{
		// combine with rule EQ
		packet p = new Packet(INITIATE, this->level+1,
								"pq", FIND) // to q
		this->send()
	}
}

node::initiate(packet* p){
	// set the state
	this->level = p->level;
	this->name = p->name;
	this->state = p->state;

	// propagate the update
	this->bestNode = NULL;
	this->bestWt = numeric_limints<int>;
	this->testNode = NULL;

	for r in neigh(this):
		status[r] = branch and r != q
			this->send(&p);

	if this->state == FIND 
		this->rec=0
		this->findMin()
}
