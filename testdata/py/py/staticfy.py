#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:49:44 2018

@author: hjh
"""

import os


def staticfy(path, name, i):
    fr_original = open(os.path.join(path, name))
    pro_orig_set = set()
    for each in fr_original.readlines():
        info = each.strip().split('\t')
        pro_orig_set.add('\t'.join(info[1:]))
    fr_original.close()
    
    fr = open(os.path.join(path + '/noise%s' % i, ('noise%s_' % i) + name))
    pro_set = set()
    for each in fr.readlines():
        info = each.strip().split('\t')
        pro_set.add('\t'.join(info[1:]))
    fr.close()
    
    print('number of interactor:', len(pro_set))
    fw = open(os.path.join(path + '/noise%s' % i, ('static_noise%s_' % i) + name), 'w')
    for each in pro_orig_set:
        fw.write('original\t' + each + '\n')
    for each in pro_set:
        fw.write('noise%s\t' % i + each + '\n')
    fw.close()
    
    
if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    for i in range(11):
        staticfy(path, 'net_960.txt', i)
    