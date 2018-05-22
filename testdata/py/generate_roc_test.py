#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:57:53 2018

@author: hjh
"""
import random
import numpy as np

fw = open('roc_test.txt', 'w')
for i in range(100):
    p = np.random.randint(0, 2, 1)[0]
    n = 1 - p
    score = np.random.random(1)[0]
    fw.write(str(p) + '\t' + str(n) + '\t' + str(score) + '\n')
fw.close()