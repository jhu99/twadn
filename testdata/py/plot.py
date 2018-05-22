#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:40:24 2018

@author: hjh
"""

from numpy import *;  
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd
import seaborn as sns

def plot(x1, y1, x2, y2, x3, y3):
    colors = 'r' 
    area = np.pi * (5)**2    
    plt.scatter(x1, y1, s=area, c=colors, alpha=0.5)
    colors = 'b' 
    area = np.pi * (5)**2    
    plt.scatter(x2, y2, s=area, c=colors, alpha=0.5)
    colors = 'y' 
    area = np.pi * (5)**2    
    plt.scatter(x3, y3, s=area, c=colors, alpha=0.5)
    plt.show()
    
    
def main():
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/test'
    f1 = open(path + '/testPair1.txt', 'r')
    f2 = open(path + '/testPair2.txt', 'r')
    f3 = open(path + '/differentPair.txt', 'r')
    x1 = range(45)
    x2 = range(45, 90)
    x3 = range(90, 190)
    y1 = []
    y2 = []
    y3 = []
    for each in f1.readlines():
        y1.append(each.strip().split(':')[1])
    for each in f2.readlines():
        y2.append(each.strip().split(':')[1])
    for each in f3.readlines():
        y3.append(each.strip().split(':')[1])
    f1.close()
    f2.close()
    f3.close()
    
    plot(x1, y1, x2, y2, x3, y3)
    
    
def heatmap():
    t = np.zeros((20, 20))
    df = pd.DataFrame(t, index=[x for x in 'abcdefghijABCDEFGHIJ'],
                  columns=[x for x in 'abcdefghijABCDEFGHIJ'])

    for x in 'abcdefghijABCDEFGHIJ':
        df[x][x] = 700




if __name__ == '__main__':
    heatmap()