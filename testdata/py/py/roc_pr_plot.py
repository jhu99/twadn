#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:56:20 2018

@author: hjh
"""
import matplotlib.pyplot as plt 
import os

def proba_sort(path, isMAG):
    xy_arr = []
    
    f1 = open(os.path.join(path, 'testPair1.txt'))
    f2 = open(os.path.join(path, 'testPair2.txt'))
    f3 = open(os.path.join(path, 'differentPair.txt'))
    
    sp = ':'
    if isMAG:
        sp = '\t'
    
    for each in f1.readlines():
        xy_arr.append([float(each.strip().split(sp)[1]), 1])
    for each in f2.readlines():
        xy_arr.append([float(each.strip().split(sp)[1]), 1])
    for each in f3.readlines():
        xy_arr.append([float(each.strip().split(sp)[1]), 0])
    
    f1.close()
    f2.close()
    f3.close()
    
    xy_arr = sorted(xy_arr, key=lambda x : x[0], reverse=True)
    return xy_arr


def plot_roc(score_mag, score_twadn):
    xy_cor = [[0, 0]]
    pre_x = 0.0
    pre_y = 0.0
    for sc, label in score_mag:
        if label == 1:
            pre_y = pre_y + (1 / 90)
        else:
            pre_x = pre_x + (1 / 100)
        xy_cor.append([pre_x, pre_y])
        
    xy_arr_tw = [[0, 0]]
    pre_xt = 0.0
    pre_yt = 0.0
    for sc, label in score_twadn:
        if label == 1:
            pre_yt = pre_yt + (1 / 90)
        else:
            pre_xt = pre_xt + (1 / 100)
        xy_arr_tw.append([pre_xt, pre_yt])
                
    x_mag = [x[0] for x in xy_cor]
    y_mag = [y[1] for y in xy_cor]
    
    x_twa = [x[0] for x in xy_arr_tw]
    y_twa = [y[1] for y in xy_arr_tw]
    #print(xy_cor)
    print('AUROC DynaMAGNA++', under_curve(x_mag, y_mag))
    print('AUROC twadn', under_curve(x_twa, y_twa))
    plt.plot(x_mag, y_mag, color='r', label='DynaMAGNA++')
    plt.plot(x_twa, y_twa, color='g', label='twadn')
    # plt.title("ROC")
    plt.xlabel("False Positive Rate", fontsize='x-large')
    plt.ylabel("True Positive Rate", fontsize='x-large')
    plt.legend(loc=8, fontsize='large')
    plt.show()
    
    
def plot_pr(score_mag, score_twadn):
    p_mag = []
    r_mag = []
    p_twadn = []
    r_twadn = []
    for i in range(190):
        tp_mag = 0.0
        fp_mag = 0.0
        tp_twa = 0.0
        fp_twa = 0.0
        for j in range(i+1):
            if score_mag[j][1] == 1:
                tp_mag += 1
            else:
                fp_mag += 1
            if score_twa[j][1] == 1:
                tp_twa += 1
            else:
                fp_twa += 1
        p_mag.append(tp_mag / (tp_mag + fp_mag))
        r_mag.append(tp_mag / 90.0)
        p_twadn.append(tp_twa / (tp_twa + fp_twa))
        r_twadn.append(tp_twa / 90.0)
        
    print('AUPR DynaMAGNA++', under_curve(r_mag, p_mag))
    print('AUPR twadn', under_curve(r_twadn, p_twadn))
    print('f1 DynaMAGNA++', get_F1(r_mag, p_mag))
    print('f1 twadn', get_F1(r_twadn, p_twadn))
    # f1_max_mag, f1_cross_mag = get_F1(r_mag, p_mag)
    # f1_max_twa, f1_cross_twa = get_F1(r_twadn, p_twadn)
    
    
    plt.plot(r_mag, p_mag, color='r', label='DynaMAGNA++')
    plt.plot(r_twadn, p_twadn, color='g', label='twadn')
    plt.xlabel("Recall", fontsize='x-large')
    plt.ylabel("Precision", fontsize='x-large')
    plt.legend(loc=8, fontsize='large')
    plt.show()
    

def under_curve(x, y):
    m = len(x)
    sqr = 0.0
    for i in range(1, m):
        sqr += 0.5 * (x[i] - x[i-1]) * (y[i] + y[i-1])
    return sqr
    

def get_F1(r, p):
    f1_max = 0.0
    f1_cross = 0.0
    dist = 1.0
    m = len(r)
    for i in range(m):
        f1 = 2 * r[i] * p[i] / (r[i] + p[i])
        if f1 > f1_max:
            f1_max = f1
        if abs(p[i] - r[i]) < dist:
            f1_cross = f1
            dist = abs(p[i] - r[i])
        # print(i, f1)
    return f1_max, f1_cross
    
    
if __name__ == '__main__':
    pathMAGNA = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/DynaMAGNA++/CLI/testPair'
    pathTWADN = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/test'
    score_mag = proba_sort(pathMAGNA, True)
    score_twa = proba_sort(pathTWADN, False)
    #print(len(score_mag))
    plot_roc(score_mag, score_twa)
    plot_pr(score_mag, score_twa)