import networkx as nx
import random
import os
import shutil


def DyGenerator(g, addNode, p, q):
    selectOne = random.sample(g.nodes(), 1)[0]
    # print('select', selectOne)
    neighbor = nx.neighbors(g, selectOne)
    # print('neighbor', neighbor)
    g.add_node(addNode)
    for each in neighbor:
        g.add_edge(each, addNode)
    for each in neighbor:
        rmEdge = random.sample([selectOne, addNode], 1)[0]
        # print('rmE', rmEdge)
        if random.uniform(0, 1) < q:
            g.remove_edge(each, rmEdge)
    if random.uniform(0, 1) < p:
        g.add_edge(selectOne, addNode)
        

def make_dyNet(path, p, q, length, nodeName):
    g = nx.Graph()
    seedNetNum = 15
    nameList = []
    for i in range(seedNetNum):
        for j in range(i + 1, seedNetNum):
            nameList.append([nodeName + '%s'%i, nodeName + '%s'%j])
    g = nx.Graph()
    g.add_edges_from(nameList)
    
    for i in range(15, 1001):
        DyGenerator(g, nodeName+'%s' % i, p, q)
        time = 1000 / length
        if i % time == 0:
            nx.write_edgelist(g, path + '/dyNetT%s.txt' % i, data=False, delimiter='\t')
            print(i, len(g.nodes()))
            


def main(path, netName):
    p = 0.7
    q = 0.6
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


def testTWADNPair(path):
    testPair = path + '/differentPair'
    net_list2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
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
            shutil.copy(dir1, testPath + '/TWADNdynet_%s.txt' % net_list1[i])
            shutil.copy(dir2, testPath + '/TWADNdynet_%s.txt' % net_list2[j])
            makeBitFile(testPath)



if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/Synthetic_Network/'
    #netName = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    #netName = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    #main(path, netName)
    #prepareForTWADN(path, netName)
    testTWADNPair(path)
   
    
    
    
    '''
    testPath = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn'
    proSet = set()
    fr1 = open(testPath + '/' + 'TWADNdynet_a1.txt')
    for pro in fr1.readlines():
        tmp = pro.strip().split('\t')
        proSet.add(tmp[1])
        proSet.add(tmp[2])
    fr2 = open(testPath + '/' + 'TWADNdynet_a2.txt')
    for pro in fr2.readlines():
        tmp = pro.strip().split('\t')
        proSet.add(tmp[1])
        proSet.add(tmp[2])
    fw = open('/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/DynaBitscore_test.txt', 'w')
    for i in proSet:
        for j in proSet:
            fw.write(i + '\t' + j + '\t' + '1e-7' +
                     '\t' + str(random.randint(90, 100)) + '\n')
    fw.close()
    fr1.close()
    '''