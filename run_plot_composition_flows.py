# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 23:43:07 2020

@author: user
"""


import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

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

with open(picklefolder + os.sep + 'dkeys.pickle', 'rb') as handle:
    dkeys = pickle.load(handle)
with open(picklefolder + os.sep + 't.pickle', 'rb') as handle:
    t = pickle.load(handle)
with open(picklefolder + os.sep + 'events_list.pickle', 'rb') as handle:
    events_list = pickle.load(handle)

# first plot tsne
plt.clf()
plt.plot(t[:,0],t[:,1], '.', markersize=1, alpha=0.3)
# then for each piece, plot on top
for i in range( 1, len( events_list ), 1 ):
    print('drawing for point: ' + str(i) + '/' + str(len(events_list)))
    ev = events_list[i]
    prev = events_list[i-1]
    if ev.pitches != -1 and prev.pitches != -1:
        # find idxs in dictionary
        ev_idx = dkeys.index( repr( ev.pitches ) )
        prev_idx = dkeys.index( repr( prev.pitches ) )
        plt.plot( [ t[ev_idx,0] , t[ prev_idx,0 ] ] , [ t[ev_idx,1] , t[ prev_idx,1 ] ], linewidth=1, alpha=0.01 )
# finally save figure
plt.savefig('composition_flows.png', dpi=500)