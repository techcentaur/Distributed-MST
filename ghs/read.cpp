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

	return 0;
}