#include <algorithm>
#include "Rel.h"
#include <iostream>
#include <unordered_map>

std::string str_add(std::string str1, std::string str2)
{
	if (str1 < str2)
	{
		return str1 + "\t" + str2;
	}
	else
	{
		return str2 + "\t" + str1;
	}
}

double distance(double* pro1, double* pro2)
{
	double res = 0;
	for (int i = 0; i < 5; i++)
	{
		res += (pro1[i] - pro2[i]) * (pro1[i] - pro2[i]);
	}
	return sqrt(res);
}

double distance_Gaussian(double* pro1, double* pro2)
{
	double res = 0;
	for (int i = 0; i < 5; i++)
	{
		res += (pro1[i] - pro2[i]) * (pro1[i] - pro2[i]);
	}
	res = exp(-(res * res) / 2);
	return res;
}
//define the function to splite a string by "\t"
std::vector<std::string> split(std::string pattern, std::string str)
{
	size_t pos;
	std::vector<std::string> result;
	str = str + pattern;
	int size = str.size();

	for (int i = 0; i < size; i++){
		pos = str.find(pattern, i);
		if (pos < size){
			std::string s = str.substr(i, pos - i);
			result.push_back(s);
			i = pos + pattern.size() - 1;
		}
	}

	return result;
}

double myMin(double a, double b, double c){
	return std::min(a, std::min(b, c));
}

// calculate the dynamic time wrapping distance of two proteins
double distance_DTW(std::vector<double*> pro1, std::vector<double*> pro2){
	int szPro1 = 0;
	int szPro2 = 0;
	
	std::vector<double*> timeSequencePro1, timeSequencePro2;

	for (int i = 0; i < pro1.size(); i++)
		if (pro1[i] != NULL){
			szPro1++;
			timeSequencePro1.push_back(pro1[i]);
		}
			
	for (int i = 0; i < pro2.size(); i++)
		if (pro2[i] != NULL){
			szPro2++;
			timeSequencePro2.push_back(pro2[i]);
		}
	// storage all distance of every two vector in a time sequence
	std::vector<std::vector<double> > dist(szPro1, std::vector<double>(szPro2, 10));

	for (int i = 0; i < szPro1; i++)
		for (int j = 0; j < szPro2; j++){
			dist[i][j] = distance(timeSequencePro1[i], timeSequencePro2[j]);
		}

	// memo[i][j] means that the DTW distance of time sequence [0,1,...,i] and [0,1,...,j]
	std::vector<std::vector<double> > memo(szPro1, std::vector<double>(szPro2, 10));
	memo[0][0] = dist[0][0];
	for (int i = 1; i < szPro2; i++)
		memo[0][i] = memo[0][i - 1] + dist[0][i];
	for (int i = 1; i < szPro1; i++)
		memo[i][0] = memo[i - 1][0] + dist[i][0];

	// cluculated all DTW by dynamic programing
	for (int i = 1; i < szPro1; i++)
		for (int j = 1; j < szPro2; j++)
			memo[i][j] = dist[i][j] + myMin(memo[i - 1][j - 1], memo[i - 1][j], memo[i][j - 1]);
	double res = memo[szPro1 - 1][szPro2 - 1];
	res = exp(-(res * res) / 2);
	return res;
}


void combineAllTop_vec(std::unordered_map<std::string, std::vector<double*> > &top_vec1,
	std::unordered_map<std::string, std::vector<double*> > &top_vec2,
	std::unordered_map<std::string, std::vector<double*> > &AllTop_vec){

	std::unordered_map<std::string, std::vector<double*> >::iterator iter;
	for (iter = top_vec1.begin(); iter != top_vec1.end(); iter++)
		AllTop_vec.insert(*iter);
	for (iter = top_vec2.begin(); iter != top_vec2.end(); iter++)
		AllTop_vec.insert(*iter);
}

void combineNetId(std::unordered_map<std::string, int> &net_protein1,
	std::unordered_map<std::string, int> &net_protein2,
	std::unordered_map<std::string, int> &allProteinNet){

	std::unordered_map<std::string, int>::iterator iter;
	for (iter = net_protein1.begin(); iter != net_protein1.end(); iter++)
		allProteinNet.insert(*iter);
	for (iter = net_protein2.begin(); iter != net_protein2.end(); iter++)
		allProteinNet.insert(*iter);
}