#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:50:45 2018

@author: hjh
"""

import networkx as nx
import random
import matplotlib.pyplot as plt 
import re
import pandas as pd
import numpy as np
import seaborn as sbs


t = np.zeros((20, 20))
df = pd.DataFrame(t, index=[x for x in 'abcdefghijABCDEFGHIJ'],
                  columns=[x for x in 'abcdefghijABCDEFGHIJ'])



path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/test'
f1 = open(path + '/testPair1_heatmap.txt', 'r')
f2 = open(path + '/testPair2_heatmap.txt', 'r')
f3 = open(path + '/differentPair_heatmap.txt', 'r')

max_score = 0.0
for each in f1.readlines():
    log = each.split(':')
    score = log[1]
    if float(score) > max_score:
        max_score = float(score)
    _in = log[0].split(' ')
    ina = _in[0]
    inb = _in[1]
    df[ina][inb] = score
    df[inb][ina] = score
    
for each in f2.readlines():
    log = each.split(':')
    score = log[1]
    if float(score) > max_score:
        max_score = float(score)
    _in = log[0].split(' ')
    ina = _in[0]
    inb = _in[1]
    df[ina][inb] = score
    df[inb][ina] = score
    
for each in f3.readlines():
    log = each.split(':')
    score = log[1]
    if float(score) > max_score:
        max_score = float(score)
    _in = log[0].split(' ')
    ina = _in[0]
    inb = _in[1]
    df[ina][inb] = score
    df[inb][ina] = score


for x in 'abcdefghijABCDEFGHIJ':
    df[x][x] = max_score
print(df)
sns.heatmap(df)
plt.show()


