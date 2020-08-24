# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 00:08:37 2020

@author: user
"""


import pickle
import os
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from ast import literal_eval
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

# test k-means
print('applying k-means')
kmeans = KMeans(n_clusters=24, random_state=0).fit(t)
# test plot k-means
plt.clf()
plt.scatter(t[:,0],t[:,1], c= kmeans.labels_.astype(float), s=10, alpha=0.1)
plt.savefig('testKMEANS.png', dpi=500)

# keep all keys for each cluster
print('keeping cluster keys')
cluster_keys = {}
for l in kmeans.labels_:
    # get indexes of label
    tmp_idxs = np.where( kmeans.labels_ == l )[0]
    tmp_keys_list = []
    for i in tmp_idxs:
        tmp_keys_list.append( literal_eval(dkeys[ i ]) )
    cluster_keys[ l ] = tmp_keys_list

# pitch class summarisation of cluster keys
print('cluster summarisation')
pc_summarisation = {}
for k in list( cluster_keys.keys() ):
    tmp_pcs = np.zeros( 12 )
    for x in cluster_keys[k]:
        if isinstance(x, list):
            for n in x:
                tmp_pcs[ n%12 ] += 1
        else:
            tmp_pcs[ x%12 ] += 1
    pc_summarisation[ k ] = tmp_pcs/sum(tmp_pcs)
    plt.clf();
    plt.bar( range( len( tmp_pcs ) ) , tmp_pcs )
    plt.savefig( 'testSummarisationCluster_' + str( k ), dpi=300 )