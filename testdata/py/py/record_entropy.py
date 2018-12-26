#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 18:39:25 2018

@author: hjh
"""

import Consistency
import os

def transform_ali(path, name, i):
    fw = open(os.path.join(path + '/noise%s' % i, 'ent_trans_' + name), 'w')
    ali = os.path.join(path + '/noise%s' % i, name)
    fr = open(ali)
    for each in fr.readlines():
        temp = each.strip().split('\t')
        if len(temp[1].split('_')) > 1:
            temp[1] = temp[1].split('_')[0]
        if len(temp[0].split('_')) > 1:
            temp[0] = temp[0].split('_')[0]
        fw.write('\t'.join(temp) + '\n')
    fr.close()
    fw.close()
        
    return os.path.join(path + '/noise%s' % i, 'ent_trans_' + name)

def record_entropy(path, name):
    fw = open(os.path.join(path, 'NetCoffee2_entropy_time.txt'), 'w')
    for i in range(11):
        # ali = os.path.join(path + '/noise%s' % i, name)
        trans_ali = transform_ali(path, name, i)
        ME = Consistency.mean_entropy('go_dick.txt', trans_ali)
        MNE = Consistency.normalized_mean_ent('go_dick.txt', trans_ali)
        fw.write('\t'.join(['noisw_level%s' % i, str(ME), str(MNE)]) + '\n')
    fw.close
    
    
if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    record_entropy(path, 'Res_Netcoffee2.ali')