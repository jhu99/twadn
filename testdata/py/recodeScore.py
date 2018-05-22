#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 09:49:27 2018

@author: hjh
"""

import os
import re

def recodeScore(testPair, pairWhat):
    filist = os.listdir(testPair)
    fw = open(testPair + '.txt', 'w')
    for eachTest in filist:
        aliPath = os.path.join(testPair, eachTest + '/Res_Pair1_%s.log' % eachTest)
        fr = open(aliPath)
        print(aliPath)
        log = fr.readlines()
        fw.write(pairWhat + ' ' + eachTest + ':' + log[-5].split(':')[1])
        fr.close()
    fw.close()
    

def reForHeatMap(testPair):
    filist = os.listdir(testPair)
    fw = open(testPair + '_heatmap.txt', 'w')
    for test in filist:
        finame = os.listdir(testPair + '/' + test)
        intactor = []
        for name in finame:
            if re.match('TWADNdynet_', name) != None:
                intactor.append(name.split('_')[1][0])
        aliPath = os.path.join(testPair + '/' + test, 'Res_Pair1_%s.log' % test)
        fr = open(aliPath)
        log = fr.readlines()
        fw.write(intactor[0] + ' ' + intactor[1] + ':' + log[-5].split(':')[1])
        fr.close()


if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/test'
    reForHeatMap(path + '/differentPair')
    #recodeScore(path + '/testPair2', 'testPair2')
        
