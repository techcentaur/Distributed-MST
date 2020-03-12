#include <iostream>
#include <fstream>
#include <vector>
#include "node.h"

using namespace std;

int main(){
	ifstream infile("input");
	
	int numNodes;
	infile >> numNodes;
	
	int a, b, wt;
	vector<edge*> edges;
	while (infile >> a >> b >> wt){
		// cout<<a<<" "<<b<<" "<<wt<<endl;
		edge e = edge(a, b, wt);
		edges.push_back(&e);
	}

	cout<<"[.] number of nodes: "<<numNodes<<endl;
	cout<<"[.] number of edges: "<<edges.size()<<endl;

	vector<node*> nodes;
	for(int i=0; i<numNodes; i++){
		node* n = new Node();
		nodes.push_back(&n);
	}

	for(int i=0; i<edges.size(); i++){
		nodes[(edges[i]->a)]->addEdge(edges[i], nodes[edges[i]->b]);
		nodes[(edges[i]->b)]->addEdge(edges[i], nodes[edges[i]->a]);
	}

	return 0;
}