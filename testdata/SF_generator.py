import networkx as nx
import random
import os
import shutil


def DyGenerator(g, addNode, p, q):
    g.add_node(addNode)
    selectOne = random.sample(g.nodes(), 1)[0]
    neighbor = nx.neighbors(g, selectOne)
    for each in neighbor:
        g.add_edge(each, addNode)
    if random.uniform(0, 1) <= p:
        g.add_edge(selectOne, addNode)
        if len(neighbor) > 1 and random.uniform(0, 1) <= q:
            selectNeighbor = random.sample(neighbor, 1)[0]
            g.remove_node(selectNeighbor)

def make_dyNet(path, p, q, length, nodeName):
    g = nx.Graph()
    g.add_edge(nodeName + '0', nodeName + '1')
    g.add_edge(nodeName + '0', nodeName + '2')
    g.add_edge(nodeName + '2', nodeName + '1')
    for i in range(3, 1000):
        DyGenerator(g, nodeName+'%s' % i, p, q)
        time = 1000 / length
        if i % time == 0:
            nx.write_edgelist(g, path + '/dyNetT%s.txt' % i, data=False, delimiter='\t')
            print(i)


def main(path, netName):
    p = 0.3
    q = 0.7
    for j in netName:
        dirPath = os.path.join(path, 'DyNet%s' % j)
        if os.path.exists(dirPath):
            make_dyNet(dirPath, p, q, 10, j)
        else:
            os.mkdir(dirPath)
            make_dyNet(dirPath, p, q, 10, j)

        print('j:', j)

def prepareForTWADN(path, netName):
    for j in netName:
        dirPath = os.path.join(path, 'DyNet%s' % j)
        if os.path.exists(dirPath):
            # fileList = os.listdir(dirPath)
            fw = open(os.path.join(dirPath, 'TWADNdynet_%s.txt' % j), 'w')
            for each in range(1, 10):
                fr = open(os.path.join(dirPath, 'dyNetT%s00.txt' % each), 'r')
                for edge in fr.readlines():
                    fw.write('dyNetT%s00.txt' % each + '\t' + edge)
                fr.close()
            fw.close()
            print(dirPath, 'finish')


def makeBitFile(testPath):
    fileList = os.listdir(testPath)
    proSet = set()
    print(fileList)
    fr1 = open(testPath + '/' + fileList[0])
    fr2 = open(testPath + '/' + fileList[1])
    for pro in fr1.readlines():
        tmp = pro.strip().split('\t')
        proSet.add(tmp[1])
        proSet.add(tmp[2])
    for pro in fr2.readlines():
        tmp = pro.strip().split('\t')
        proSet.add(tmp[1])
        proSet.add(tmp[2])
    fw = open(testPath + '/' + 'DynaBitscore.txt', 'w')
    for i in proSet:
        for j in proSet:
            fw.write(i + '\t' + j + '\t' + '1e-7' +
                     '\t' + str(random.randint(90, 100)) + '\n')
    fw.close()
    fr1.close()
    fr2.close()


def testTWADNPair(path, netName):
    testPair = path + '/diffetenttPair'
    net_list2 = netName
    net_list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    cnt = 0
    for i in range(10):
        for j in range(10):
            testPath = os.path.join(testPair + '/test%s' % cnt)
            cnt += 1
            if not os.path.exists(testPath):
                os.mkdir(testPath)
            dir1 = os.path.join(path, 'p0.3_q0.7/DyNet%s/TWADNdynet_%s.txt' %
                                (net_list1[i], net_list1[i]))
            dir2 = os.path.join(path, 'p0.7_q0.6/DyNet%s/TWADNdynet_%s.txt' %
                                (net_list2[j], net_list2[j]))
            shutil.copy(dir1, testPath + '/TWADNdynet_%s1.txt' % net_list1[i])
            shutil.copy(dir2, testPath + '/TWADNdynet_%s2.txt' % net_list2[j])

            makeBitFile(testPath)



if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/Synthetic_Network'
    netName = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    #netName = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    #main(path, netName)
    #prepareForTWADN(path, netName)
    testTWADNPair(path, netName)