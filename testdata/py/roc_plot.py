#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:56:20 2018

@author: hjh
"""
import matplotlib.pyplot as plt 
import os

def proba_sort(path):
    xy_arr = []
    
    f1 = open(os.path.join(path, 'testPair1.txt'))
    f2 = open(os.path.join(path, 'testPair2.txt'))
    f3 = open(os.path.join(path, 'differentPair.txt'))
    
    for each in f1.readlines():
        xy_arr.append([float(each.strip().split(':')[1]), 1])
    for each in f2.readlines():
        xy_arr.append([float(each.strip().split(':')[1]), 1])
    for each in f3.readlines():
        xy_arr.append([float(each.strip().split(':')[1]), 0])
    
    f1.close()
    f2.close()
    f3.close()
    
    xy_arr = sorted(xy_arr, key=lambda x : x[0], reverse=True)
    return xy_arr


def plot_roc(score):
    xy_cor = [[0, 0]]
    pre_x = 0.0
    pre_y = 0.0
    for sc, label in score:
        if label == 1:
            pre_y = pre_y + (1 / 90)
        else:
            pre_x = pre_x + (1 / 100)
        xy_cor.append([pre_x, pre_y])
            
    x = [x[0] for x in xy_cor]
    y = [y[1] for y in xy_cor]
    #print(xy_cor)
    plt.plot(x, y)
    plt.show()
    
if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/test'
    score = proba_sort(path)
    plot_roc(score)
    