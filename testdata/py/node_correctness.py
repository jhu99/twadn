#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:33:14 2018

@author: hjh
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import plot_noise_time


def normalization(score):
    _max = 0.0
    _min = 10000.0
    for i in range(11):
        if score[i] > _max:
            _max = score[i]
        if _min < score[i]:
            _min = score[i]
    for i in range(11):
        score[i] = (score[i] - _min) / (_max - _min)
    return score

def node_correctness(path):
    fr = open(path)
    ali = fr.readlines()
    number_of_matchset = len(ali)
    number_of_correct = 0.0
    for each in ali:
        pro = each.strip().split('\t')
        pro1 = pro[0]
        pro2 = pro[1]
        if 'noise' in pro[0]:
            pro1 = pro[0].split('_')[0]
        else:
            pro2 = pro[1].split('_')[0]
        if pro1 == pro2:
            number_of_correct += 1
    print('number_of_matchset', number_of_matchset)
    print('number_of_correct', number_of_correct)
    print('correctness:', number_of_correct / number_of_matchset)
    return number_of_correct / number_of_matchset


def record_node_correctness(path):
    twadn_correctness = []
    netcoffee_correnctness = []
    for i in range(11):
        twadn_ali = os.path.join(path, 'noise%s/Res_str.ali' % i)
        netcoffee_ali = os.path.join(path, 'noise%s/Res_Netcoffee2_str.ali' % i)
        twadn_correctness.append(node_correctness(twadn_ali))
        netcoffee_correnctness.append(node_correctness(netcoffee_ali))
        
    return twadn_correctness, netcoffee_correnctness


def plot_node_correctness(twadn_ct, netcf_ct):
    x = []
    for i in range(11):
        x.append(i / 10.0)
        
    plt.plot(x, twadn_ct, color='g', label='twadn')
    plt.plot(x, netcf_ct, color='r', label='NetCoffee2')
    plt.xlabel('Noise Level', fontsize='x-large')
    plt.ylabel('Node Correctness', fontsize='x-large')
    plt.legend(loc=8, fontsize='large')
    plt.yticks(np.arange(0, 1, 0.1))
    
    plt.show()
    

if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/twadn'
    twadn_correctness, netcoffee_correnctness = record_node_correctness(path)
    plot_noise_time(path + '/twadn_str.txt',
                    path + '/NetCoffee2_str.txt')
    #twadn_correctness = normalization(twadn_correctness)
    #netcoffee_correnctness = normalization(netcoffee_correnctness)
    plot_node_correctness(twadn_correctness, netcoffee_correnctness)