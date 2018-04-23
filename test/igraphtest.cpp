#include <iostream>
#include "ReadDynaPPI.h"
#include "argparser.h"
#include "ReadBitscore.h"
#include "Alignment.h"
#include "simulate.h"
#include <time.h>
#include <fstream>
#include <unordered_map>
//using namespace std;

int main()
{
	clock_t start = clock();

	std::ofstream out("testOut.log");
	std::streambuf *coutbuf = std::cout.rdbuf(); //save old buf
	std::cout.rdbuf(out.rdbuf()); //redirect std::cout to out.txt!

	ReadDynaPPI net1("DynaNet1.txt", 5, 1);
	net1.calculate_topologyVector();
	ReadDynaPPI net2("DynaNet2.txt", 5, 2);
	net2.calculate_topologyVector();

	std::unordered_map<std::string, std::vector<double*> > AllTop_vec;
	combineAllTop_vec(net1.top_vec, net2.top_vec, AllTop_vec);

	ReadBitscore bitscore("11.txt", AllTop_vec, 0.5, 1e-7);

	std::cout << "# bitscore.protein_score.size():" << bitscore.protein_score.size() << std::endl;
	std::unordered_map<std::string, score*>::iterator *candidates = new
		std::unordered_map<std::string, score*>::iterator[bitscore.protein_score.size()];
	bitscore.colected_candidates(1, candidates);

	std::unordered_map<std::string, int> Allnet_protein;
	combineNetId(net1.net_protein, net2.net_protein, Allnet_protein);

	std::cout << "size" << Allnet_protein.size() << std::endl;
	std::unordered_map<std::string, int>::iterator iter;
	for (iter = Allnet_protein.begin(); iter != Allnet_protein.end(); iter++)
		std::cout << iter->first << " :" << iter->second << std::endl;

	Alignment Ali(&Allnet_protein, &bitscore.protein_score, bitscore.m_dMeanf);
	sumulate sim(10, 100, 10, bitscore.can_size, candidates, &Ali, "testOut.txt");
	sim.start(out);

	delete[] candidates;
	candidates = NULL;
	clock_t ends = clock();
	std::cout << "# Running Time : " << (double)(ends - start) / CLOCKS_PER_SEC << std::endl;
	std::cout.rdbuf(coutbuf); //reset to standard output again
	std::cout << "done..." << std::endl;


	return 0;
}


//#include <iostream>
//#include <array>
//#include "ReadDynaPPI.h"
//#include "argparser.h"
//#include "ReadBitscore.h"
//#include "Alignment.h"
//#include "simulate.h"
//#include <time.h>
//#include <fstream>
//
//using namespace std;
//
//
//struct Option{
//	std::string inputfilename_net1;
//	std::string inputfilename_net2;
//	std::string inputfilename_bit;
//	int length1;
//	int length2;
//	std::string outputfilename;
//	double aplh;
//	double beta;
//	double evalue;
//	bool help;
//	bool version;
//	Option(){
//	}
//};
//
//int main(int argc, const char * argv[])
//{
//
//
//	ArgParser mf_parser;
//	Option mf_option;
//
//	//Parser the argument
//	mf_parser.setName("NetCoffee2", "An application for multiple global network alignment.");
//	mf_parser.setVerion("1.0.006");
//	mf_parser.refOption("help", "Show help information.", mf_option.help);
//	mf_parser.refOption("version", "Show the current version.", mf_option.version);
//	mf_parser.refOption("inputnet1", "The path of an input file.", mf_option.inputfilename_net1, "", true);
//	mf_parser.refOption("inputnet2", "The path of an input file.", mf_option.inputfilename_net2, "", true);
//	mf_parser.refOption("inputbit", "The path of an input file.", mf_option.inputfilename_bit, "", true);
//	mf_parser.refOption("net1Length", "The number of ppi networks", mf_option.length1, 1, true);
//	mf_parser.refOption("net2Length", "The number of ppi networks", mf_option.length2, 1, true);
//	mf_parser.refOption("output", "The path of an output file.", mf_option.outputfilename, "", true);
//	mf_parser.refOption("alph", "alph for sequence and topology similarity", mf_option.aplh, 0.5);
//	mf_parser.refOption("beta", "beta used for the rate of conserved protein in a same network", mf_option.beta, 2);
//	mf_parser.refOption("evalue", "evalue used to pick the sequence similarity which has a lower e-value than evalue", mf_option.evalue, 1e-7);
//
//	if (!mf_parser.run(argc, argv))
//		return 1;
//	clock_t start = clock();
//
//	std::ofstream out(mf_option.outputfilename + ".log");
//	std::streambuf *coutbuf = std::cout.rdbuf(); //save old buf
//	std::cout.rdbuf(out.rdbuf()); //redirect std::cout to out.txt!
//
//	ReadDynaPPI net1(mf_option.inputfilename_net1, mf_option.length1, 1);
//	net1.calculate_topologyVector();
//	ReadDynaPPI net2(mf_option.inputfilename_net2, mf_option.length2, 2);
//	net2.calculate_topologyVector();
//
//	std::unordered_map<std::string, std::vector<double*> > AllTop_vec;
//	combineAllTop_vec(net1.top_vec, net2.top_vec, AllTop_vec);
//
//	ReadBitscore bitscore(mf_option.inputfilename_bit, AllTop_vec, mf_option.aplh, mf_option.evalue);
//
//	cout << "# bitscore.protein_score.size():" << bitscore.protein_score.size() << endl;
//	unordered_map<string, score*>::iterator *candidates = new
//		unordered_map<string, score*>::iterator[bitscore.protein_score.size()];
//	bitscore.colected_candidates(mf_option.beta, candidates);
//
//	std::unordered_map<std::string, int> Allnet_protein;
//	combineNetId(net1.net_protein, net2.net_protein, Allnet_protein);
//	Alignment Ali(&Allnet_protein, &bitscore.protein_score, bitscore.m_dMeanf);
//	sumulate sim(1000, 100, 10, bitscore.can_size, candidates, &Ali, mf_option.outputfilename);
//	sim.start(out);
//
//	delete[] candidates;
//	candidates = NULL;
//	clock_t ends = clock();
//	cout << "# Running Time : " << (double)(ends - start) / CLOCKS_PER_SEC << endl;
//	std::cout.rdbuf(coutbuf); //reset to standard output again
//	std::cout << "done..." << std::endl;
//	return 0;
//}