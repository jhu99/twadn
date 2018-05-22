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
        

def make_dyNet(path, p, q, nodeName):
    g = nx.Graph()
    seedNetNum = 15
    nameList = []
    for i in range(seedNetNum):
        for j in range(i + 1, seedNetNum):
            nameList.append([nodeName + '%s'%i, nodeName + '%s'%j])
    g = nx.Graph()
    g.add_edges_from(nameList)
    
    i = 15
    while True:
        DyGenerator(g, nodeName+'%s' % i, p, q)
        g = max(nx.connected_component_subgraphs(g), key=len)
        num_nodes = len(g)
        if num_nodes % 100 == 0:
            nx.write_edgelist(g, path + '/dyNetT%s.txt' % num_nodes,
                              data=False, delimiter='\t')
            print('sub len:', num_nodes, 'i:', i)
        i += 1
        if num_nodes > 1000:
            break

def main(path, netName):
    p = 0.7
    q = 0.6
    for nodeN in netName:
        dirPath = os.path.join(path, 'DyNet%s' % nodeN)
        if os.path.exists(dirPath):
            make_dyNet(dirPath, p, q, nodeN)
        else:
            os.mkdir(dirPath)
            make_dyNet(dirPath, p, q, nodeN)

        print('nodeN:', nodeN)

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
    testPair = path + '/testPair2'
    net_list2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    net_list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    cnt = 0
    for i in range(10):
        for j in range(i+1, 10):
            testPath = os.path.join(testPair + '/test%s' % cnt)
            cnt += 1
            if not os.path.exists(testPath):
                os.mkdir(testPath)
            dir1 = os.path.join(path, 'p0.7_q0.6/DyNet%s/TWADNdynet_%s.txt' %
                                (net_list2[i], net_list2[i]))
            dir2 = os.path.join(path, 'p0.7_q0.6/DyNet%s/TWADNdynet_%s.txt' %
                                (net_list2[j], net_list2[j]))
            shutil.copy(dir1, testPath + '/TWADNdynet_%s.txt' % net_list2[i])
            shutil.copy(dir2, testPath + '/TWADNdynet_%s.txt' % net_list2[j])
            makeBitFile(testPath)




if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/Synthetic_Network'
    netName = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
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