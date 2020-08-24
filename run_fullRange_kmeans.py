# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:47:48 2020

@author: user
"""

import pickle
import os
import numpy as np
from sklearn.cluster import KMeans
from ast import literal_eval
import matplotlib.pyplot as plt

num_clusters = 48

picklefolder = 'pickles' + os.sep + 'data_as_a_sequence'

with open(picklefolder + os.sep + 'context_matrix.pickle', 'rb') as handle:
    context_matrix = pickle.load(handle)
with open(picklefolder + os.sep + 'dkeys.pickle', 'rb') as handle:
    dkeys = pickle.load(handle)
with open(picklefolder + os.sep + 't.pickle', 'rb') as handle:
    t = pickle.load(handle)

# test k-means
print('applying k-means')
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(t)
# test plot k-means
plt.clf()
plt.scatter(t[:,0],t[:,1], c= kmeans.labels_.astype(float), s=1, alpha=0.1)
plt.savefig('testKMEANS.png', dpi=500)

# keep all keys for each cluster
print('keeping cluster keys')
cluster_keys = {}
# keep unique labels
unique_labels = range( num_clusters )
for l in unique_labels:
    # print('cluster label: ' + str(l))
    # get indexes of label
    tmp_idxs = np.where( kmeans.labels_ == l )[0]
    tmp_keys_list = []
    for c_i, i in enumerate(tmp_idxs):
        print('cluster label: ' + str(l) + ' - ' + str(c_i) + '/' + str(len(tmp_idxs)))
        tmp_keys_list.append( literal_eval(dkeys[ i ]) )
    cluster_keys[ l ] = tmp_keys_list

# pitch class summarisation of cluster keys
print('cluster summarisation')
pc_summarisation = {}
for k in list( cluster_keys.keys() ):
    tmp_pcs = np.zeros( 128 )
    for x in cluster_keys[k]:
        if isinstance(x, list):
            for n in x:
                tmp_pcs[ n ] += 1
        else:
            tmp_pcs[ x ] += 1
    pc_summarisation[ k ] = tmp_pcs/sum(tmp_pcs)
    plt.clf();
    plt.bar( range( len( tmp_pcs ) ) , tmp_pcs )
    plt.savefig( 'testSummarisationCluster_' + str( k ), dpi=300 )