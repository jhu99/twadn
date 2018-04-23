#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <igraph.h>
#include <cassert>
#include "ReadDynaPPI.h"


ReadDynaPPI::ReadDynaPPI(std::string DynaNet, int timeLength, int netid)
{
	m_iNumNets = timeLength;
	m_vecEdges = new std::vector<std::string>[m_iNumNets];
	m_umap_vectex = new std::unordered_map<std::string, int>[m_iNumNets];
	m_umap_pro = new std::unordered_map<int, std::string>[m_iNumNets];
	std::ifstream in(DynaNet);
	if (!in){
		std::cout << "# can't open net..." << std::endl;
		assert(false);
	}//read network form file

	std::string temp[3];
	int i = 0;
	int netId = -1;
	std::string net = "ID";
	std::unordered_map<std::string, int>::iterator ver;
	std::unordered_map<int, std::string>::iterator pro;
	std::cout << "# reading network..." << std::endl;
	while (in >> temp[0] && in >> temp[1] && in >> temp[2])
	{
		// record all proteins in m_uset_protein
		m_uset_allProtein.insert(temp[1]);
		m_uset_allProtein.insert(temp[2]);

		net_protein[temp[1]] = netid;
		net_protein[temp[2]] = netid;
		if (temp[0] != net)
		{
			netId++;
			net = temp[0];
			id_nets.push_back(net);
			igraph_t igraph;
			m_igraph.push_back(igraph);
			i = 0;
		}
		m_vecEdges[netId].push_back(temp[1]);
		m_vecEdges[netId].push_back(temp[2]);
		if (m_umap_vectex[netId].find(temp[1]) == m_umap_vectex[netId].end())
		{
			m_umap_vectex[netId][temp[1]] = i;
			m_umap_pro[netId][i] = temp[1];
			i++;
		}
		if (m_umap_vectex[netId].find(temp[2]) == m_umap_vectex[netId].end())
		{
			m_umap_vectex[netId][temp[2]] = i;
			m_umap_pro[netId][i] = temp[2];
			i++;
		}
	}

	igraph_vector_t *edge_vec = new igraph_vector_t[m_iNumNets];
	for (int p = 0; p < m_iNumNets; p++)
	{
		igraph_vector_init(&edge_vec[p], m_vecEdges[p].size());
		int k = 0;
		for (auto q : m_vecEdges[p])
		{
			VECTOR(edge_vec[p])[k] = m_umap_vectex[p][q];
			k++;
		}
		igraph_create(&m_igraph[p], &edge_vec[p], m_umap_vectex[p].size(), 0);
		igraph_simplify(&m_igraph[p], 1, 1, 0);
		std::cout << "# number of vertex in " << id_nets[p] << ": " << igraph_vcount(&m_igraph[p]) << std::endl;
		std::cout << "# number of edges in " << id_nets[p] << ": " << igraph_ecount(&m_igraph[p]) << std::endl;
	}
	delete edge_vec;
	edge_vec = NULL;
}

ReadDynaPPI::~ReadDynaPPI()
{
	delete[] m_vecEdges;
	m_vecEdges = NULL;
	delete[] m_umap_pro;
	m_umap_pro = NULL;
	delete[]m_umap_vectex;
	m_umap_vectex = NULL;

	std::unordered_map<std::string, std::vector<double*> >::iterator it;
	for (it = top_vec.begin(); it != top_vec.end(); it++)
	{
		for (int i = 0; i < m_iNumNets; i++){
			if (it->second[i] != NULL){
				delete[] it->second[i];
				it->second[i] = NULL;
			}
		}
	}

}

void ReadDynaPPI::calculate_topologyVector()
{
	std::cout << "# begin calculate every protein in PPI networks" << std::endl;

	//initial the top_vec, each protein map a vector, which contain m_inumNets NULL;
	std::unordered_set<std::string>::iterator iter;
	for (iter = m_uset_allProtein.begin(); iter != m_uset_allProtein.end(); iter++)
		top_vec[*iter] = std::vector<double*>(m_iNumNets, NULL);

	for (int p = 0; p < m_iNumNets; p++)
	{
		const int num_v = igraph_vcount(&m_igraph[p]);
		unsigned short *adj_matrix = new unsigned short[num_v * num_v]();
		unsigned short *adj_matrix_2 = new unsigned short[num_v * num_v]();

		double *engin = new double[num_v]();
		igraph_adjlist_t al;
		igraph_adjlist_init(&m_igraph[p], &al, IGRAPH_OUT);

		//initial adjcent matrix 
		for (int i = 0; i < num_v; i++)
		{
			igraph_vector_int_t *temp;
			temp = igraph_adjlist_get(&al, i);
			int size = igraph_vector_int_size(temp);
			for (int j = 0; j < size; j++)
			{
				adj_matrix[i * num_v + (VECTOR(*temp)[j])] = 1;
			}
		}

		//calculate engine of adjcent matrix
		double *te_en = new double[num_v]();
		for (int i = 0; i < num_v; i++)
		{
			for (int j = 0; j < num_v; j++)
			{
				te_en[i] += adj_matrix[i * num_v + j];
			}
			//std::cout << "te_en:" << i << " " << te_en[i] << " " << std::endl;
		}

		for (int i = 0; i < num_v; i++)
		{
			for (int j = 0; j < num_v; j++)
			{
				if (te_en[j] != 0)
				{
					engin[i] += adj_matrix[i * num_v + j] / te_en[j];
				}
			}

		}
		delete[]te_en;
		te_en = NULL;

		//calculate all distance of two vertice in network

		for (int i = 0; i < num_v; i++)
		{
			for (int j = 0; j < num_v; j++)
			{
				if (adj_matrix[i * num_v + j] != 0)
				{
					for (int k = 0; k < num_v; k++)
					{
						if (adj_matrix[j*num_v + k] != 0)
						{
							adj_matrix_2[i * num_v + k] += adj_matrix[i * num_v + j] * adj_matrix[j * num_v + k];
						}
					}
				}
			}
		}

		//calculate the topology vector of every vertex
		std::vector<double> max_vector(5, 0);
		for (int i = 0; i < num_v; i++)
		{
			int frist = 0, second = 0;
			bool* b_frist = new bool[num_v]();
			double frist_rep = 0, second_rep = 0;
			double* temp = new double[5];
			temp[0] = engin[i];

			for (int j = 0; j < num_v; j++)
			{
				if (adj_matrix[i * num_v + j] != 0)
				{
					frist++;
					b_frist[j] = true;
					frist_rep += engin[j];
				}
			}
			for (int j = 0; j < num_v; j++)
			{
				if (adj_matrix_2[i * num_v + j] != 0)
				{
					if (!b_frist[j] && j != i)
					{
						second++;
						second_rep += engin[j] * adj_matrix_2[i * num_v + j] / 2;
					}
				}
			}

			temp[1] = frist;
			temp[2] = frist_rep;
			temp[3] = second;
			temp[4] = second_rep;
			for (int b = 0; b < 5; b++)
			{
				if (temp[b] > max_vector[b])
					max_vector[b] = temp[b];
			}
			std::string protein = m_umap_pro[p][i];
			top_vec[protein][p] = temp;

			delete[] b_frist;
			b_frist = NULL;
		}

		std::cout << "# max_vec::" << max_vector[0] << " " << max_vector[1] << " " << max_vector[2] << " "
			<< max_vector[3] << " " << max_vector[4] << std::endl;

		for (int i = 0; i < num_v; i++)
		{
			std::string new_protein = m_umap_pro[p][i];
			//double *new_temp = top_vec[new_protein];
			for (int x = 0; x < 5; x++)
			{
				if (max_vector[x] != 0)
					top_vec[new_protein][p][x] = top_vec[new_protein][p][x] / max_vector[x];
			}
		}

		delete[] engin;
		engin = NULL;

		delete[]adj_matrix;
		adj_matrix = NULL;

		delete[]adj_matrix_2;
		adj_matrix_2 = NULL;
		std::cout << "# " << id_nets[p] << "  done..." << std::endl;
	}

}