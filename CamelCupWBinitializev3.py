# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 21:03:44 2019

@author: Connor
"""

'''Use ReLu for weight and bias initialization'''

import random
import numpy as np
import operator
from functools import wraps
import pickle

neurons = [32,90,90,90,16]

'''Initialize zero matrices'''
layers = len(neurons)-1
y = 0

randdict={}
        
for x in range(layers):
    randdict["wmat{0}".format(y+1)] = np.zeros(shape=(neurons[y+1],neurons[y]))
    randdict["bmat{0}".format(y+1)] = np.zeros(shape=(neurons[y],1))
    y = y + 1

for s in range(len(neurons)-1):
    currentlayer = neurons[s+1]
    layerbefore = neurons[s]
    randdict["wmat{0}".format(s+1)] = np.random.randn(neurons[s+1],neurons[s]) * np.sqrt(2/neurons[s])
    randdict["bmat{}".format(s+1)] = np.random.randn(neurons[s+1],1) * np.sqrt(2/neurons[s])

with open('CamelCupNNweightsbiasv1.pickle', 'wb') as handle:
    pickle.dump(randdict, handle, protocol=pickle.HIGHEST_PROTOCOL)