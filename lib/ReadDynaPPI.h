#ifndef ReadPPI_h
#define ReadPPI_h

#include <igraph.h>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

class ReadDynaPPI
{
public:
	ReadDynaPPI(std::string DynaNet, int timeLength, int netid);
	~ReadDynaPPI();
	// storage all protein and its time sequence egine vector
	std::unordered_map<std::string, std::vector<double*> > top_vec;
	void calculate_topologyVector();
	std::unordered_map<std::string, int> net_protein;

private:
	int m_iNumNets;
	std::vector<igraph_t> m_igraph;
	std::vector<std::string> *m_vecEdges;
	std::unordered_map<std::string, int> *m_umap_vectex;
	std::unordered_map<int, std::string> *m_umap_pro;
	std::vector<std::string> id_nets;
	std::unordered_set<std::string> m_uset_allProtein;
};

#endif