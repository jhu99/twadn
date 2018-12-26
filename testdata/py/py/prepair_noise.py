#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 21:22:31 2018

@author: hjh
"""

import os


def prepair_noise(path, noise_level):
    fr_net = open(os.path.join(path, 'bit_twadn_960.txt'))
    fw_net = open(os.path.join(path + '/noise%s' % noise_level,
                               'noise%s_bit_960.txt' % noise_level), 'w')
    
    for each in fr_net.readlines():
        info = each.strip().split('\t')
        fw_net.write('\t'.join([info[0], info[1][:-7] + '_noise_%s' % noise_level,
                                info[2], info[3]]) + '\n')
    fr_net.close()
    fw_net.close()
    
    

if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    for i in range(4):
        prepair_noise(path, i)