#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 19:40:38 2018

@author: hjh
"""
import matplotlib.pyplot as plt 


def normalization(score):
    _max = 0.0
    _min = 10000.0
    for i in range(11):
        if score[i] > _max:
            _max = score[i]
        if score[i] < _min:
            _min = score[i]
    print(_max, _min)
    for i in range(11):
        score[i] = (score[i] - _min) / (_max - _min)
    return score


def plot_noise_time(path_twadn, path_netcoffee):
    fr_twadn = open(path_twadn)
    fr_netcoffee = open(path_netcoffee)
    
    ali_score_twadn = []
    ali_score_netcoffee = []
    
    for each in fr_twadn.readlines():
        info = each.strip().split('\t')
        if len(info) > 1:
            ali_score_twadn.append(float(info[2]))
    
    for each in fr_netcoffee.readlines():
        info = each.strip().split('\t')
        if len(info) > 1:
            ali_score_netcoffee.append(float(info[2]))
            
    fr_netcoffee.close()
    fr_twadn.close()
    
    #print(ali_score_netcoffee)
    #ali_score_netcoffee = normalization(ali_score_netcoffee)
    #print(ali_score_netcoffee)
    #ali_score_twadn = normalization(ali_score_twadn)
    
    x= []
    for i in range(11):
        x.append(i / 10.0)
    
        
    plt.plot(x, ali_score_twadn, color='g', label='twadn')
    plt.plot(x, ali_score_netcoffee, color='r', label='netcoffee')
    #plt.title("noise")
    plt.xlabel("Noise Level", fontsize='x-large')
    plt.ylabel("Alignment Score", fontsize='x-large')
    plt.legend(loc=8, fontsize='x-large')
    #plt.yticks(np.arange(0, 0.5, 0.1))
    plt.show()
    
if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    plot_noise_time(path + '/twadn_time.txt',
                    path + '/NetCoffee2_time.txt',)
    
    
    
