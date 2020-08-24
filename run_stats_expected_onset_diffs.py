# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 07:40:38 2020

@author: user
"""

import pickle
import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import math

# This script prepares a graph showing the onset time differences between
# all current notes and their immediate previous and next notes
# Aim is to figure out a rational value for exponential decrease of the impact
# of chromatic context when moving away from the note of interest

picklefolder = 'pickles' + os.sep + 'data_as_a_sequence'

class MusicEvent:
    def __init__(self, m21_note):
        if m21_note == 'start':
            self.pitches = -1
            self.offset = -1
            self.duration = -1
            self.velocity = -1
        elif m21_note.isChord:
            self.pitches = [p.midi for p in m21_note.pitches]
            self.offset = float( m21_note.offset )
            self.duration = float( m21_note.duration.quarterLength )
            self.velocity = float( m21_note.volume.velocity )
        elif m21_note.isNote:
            self.pitches = m21_note.pitch.midi
            self.offset = float( m21_note.offset )
            self.duration = float( m21_note.duration.quarterLength )
            self.velocity = float( m21_note.volume.velocity )
    # end constructor
# end MusicEvent class

with open(picklefolder + os.sep + 'events_list.pickle', 'rb') as handle:
    events_list = pickle.load(handle)

iois = []

for i in range( 1 , len( events_list )-1 , 1 ):
    if events_list[i].offset != -1:
        if events_list[i-1].offset != -1:
            iois.append( events_list[i-1].offset - events_list[i].offset )
        if events_list[i+1].offset != -1:
            iois.append( events_list[i+1].offset - events_list[i].offset )

c = Counter( iois )
k = np.array( list( c.keys() ) )
v = np.array( list( c.values() ) )
# find values of v that are above 10% of averate
thrsh = 0.1*np.mean(v)
tmp_idxs = np.where( v > thrsh )[0]
v1 = v[tmp_idxs.astype(int)]
k1 = k[tmp_idxs.astype(int)]
v1 = v1 / np.sum( v1 )

# gaussian fit
x = k1
y = v1
mean_gauss = sum(k1*v1)
sigma_gauss = sum(v1*(k1-mean_gauss)**2)
# dialate sigma
sigma_gauss *= 3

x = k1
a = 1/(sigma_gauss*np.sqrt(2)*math.pi)
y = a*np.exp( -(1/2)*np.power( (x-mean_gauss)/sigma_gauss , 2 ) )
# y = y/np.max(y)

plt.clf()
plt.bar( k1 , v1, width=0.125 )
plt.plot( x , y , 'ro' )
plt.savefig('test_offsetdiff_stats.png', dpi=300)

with open(picklefolder + os.sep + 'mean_gauss.pickle', 'wb') as handle:
    pickle.dump(mean_gauss, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(picklefolder + os.sep + 'sigma_gauss.pickle', 'wb') as handle:
    pickle.dump(sigma_gauss, handle, protocol=pickle.HIGHEST_PROTOCOL)