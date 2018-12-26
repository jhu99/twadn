#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:41:18 2018

@author: hjh
"""

import os


def record(path, name_log, name_ali):
    fr_log = open(os.path.join(path, name_log))
    fr_ali = open(os.path.join(path, name_ali))
    log = fr_log.readlines()
    score = float(log[-5].split(':')[1])
    ali = fr_ali.readlines()
    mean_score = score / float(len(ali))
    return score, mean_score
'''
def record_netcoffee2(path, name):
    fr = open(os.path.join(path, name))
    log = fr.readlines()
    score = log[-5].split(':')[1]
    return score
'''


if __name__ == '__main__':
    fw = open('../net_9606/twadn_str.txt', 'w')
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    for i in range(11):
        noise = 'noise%s' % i
        score, mean_score = record(path, noise + '/Res_str.log',
                                   noise + '/Res_str.ali')
        fw.write(noise + '\t' + str(score) + '\t' + str(mean_score) + '\n')
        print(noise, score, mean_score)
    fw.close()