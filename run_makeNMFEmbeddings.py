import os
import pickle
import numpy as np
from sklearn.manifold import TSNE
from scipy.spatial import distance

picklefolder = 'pickles'

with open(picklefolder + os.sep + 'r_parts.pickle', 'rb') as handle:
    r_parts = pickle.load(handle)

with open(picklefolder + os.sep + 's_cnt.pickle', 'rb') as handle:
    s_cnt = pickle.load(handle)

# construct dictionary from s_cnt
d = {}
# add start and end entries - assuming 0 appearances
d['s'] = 0
d['e'] = 0
for c in s_cnt:
    d[ c[0] ] = c[1]

# define context window size
w = 4

# keep keys
d_keys = list( d.keys() )

# for each part, initially assume a w-tuple of start instances and a w-tuple at the end
# keep sequences of indexes - adding start and end
idx_parts = []

# construct parts as indexes - with starting and ending
# keep number of data points
num_points = 0
for i,p in enumerate( r_parts ):
    print('constructing indexes of ' + str(i) + '/' + str(len(r_parts)))
    idx_part = []
    # add starting prefix
    for i in range(w):
        idx_part.append( d_keys.index( 's' ) )
        num_points += 1
    for r in p:
        idx_part.append( d_keys.index( r ) )
        num_points += 1
    # add ending prefix
    for i in range(w):
        idx_part.append( d_keys.index( 'e' ) )
        num_points += 1
    # print( repr(idx_part) )
    idx_parts.append( idx_part )

print('number of data points: ' + str(num_points))
# construct empty space
full_space = np.zeros( ( len(d_keys), len(d_keys) ), dtype=np.uint16 )
print('full space dimensionality: ' + repr(full_space.shape))

# fill full space
print('filling space')
for i_p, p in enumerate( idx_parts ):
    print( 'idx part ' + str(i_p) + ' of ' + str(len(idx_parts)) )
    for i in range( w, len(p)-w, 1 ):
        full_space[ i , p[ i-w : i ] ] += 1
        full_space[ i , p[ i+1 : i+w+1 ] ] += 1

dst = distance.pdist( full_space )
sqdst = distance.squareform( dst )

# print('running tsne')
# running tsne
# X_embedded = TSNE(n_components=2, verbose=5).fit_transform(full_space)