# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:03:59 2020

@author: user
"""


import pickle
import os
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
# from collections import Counter

picklefolder = 'pickles' + os.sep + 'data_as_a_sequence'

with open(picklefolder + os.sep + 'context_matrix.pickle', 'rb') as handle:
    context_matrix = pickle.load(handle)
with open(picklefolder + os.sep + 'dkeys.pickle', 'rb') as handle:
    dkeys = pickle.load(handle)

# TSNE
t = TSNE(n_components=2, verbose=10).fit_transform(context_matrix)
plt.clf()
plt.plot(t[:,0],t[:,1], '.', markersize=1, alpha=0.3)
plt.savefig('testTSNE.png', dpi=500)

with open(picklefolder + os.sep + 't.pickle', 'wb') as handle:
    pickle.dump(t, handle, protocol=pickle.HIGHEST_PROTOCOL)
