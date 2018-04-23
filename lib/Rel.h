#include <string>
#include <cmath>
#include <vector>
#include <unordered_map>
#pragma once

struct score
{
	double bitscore;
	double topscore;
	double finalscore;
};


std::string str_add(std::string str1, std::string str2);

double distance(double* pro1, double* pro2);

double distance_Gaussian(double* pro1, double* pro2);

std::vector<std::string> split(std::string pattern, std::string str);

double distance_DTW(std::vector<double*> pro1, std::vector<double*> pro2);

// combine two top_vec
// storage all protein and its eigen vector in a map
void combineAllTop_vec(std::unordered_map<std::string, std::vector<double*> > &top_vec1,
	std::unordered_map<std::string, std::vector<double*> > &top_vec2,
	std::unordered_map<std::string, std::vector<double*> > &AllTop_vec);

// record every protein belone to which species
void combineNetId(std::unordered_map<std::string, int> &net_protein1,
	std::unordered_map<std::string, int> &net_protein2,
	std::unordered_map<std::string, int> &allProteinNet);