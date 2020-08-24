# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:02:32 2020

@author: user
"""


import pickle
import os
import numpy as np
import math

picklefolder = 'pickles' + os.sep + 'data_as_a_sequence'
# context length
w = 5

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

with open(picklefolder + os.sep + 'mean_gauss.pickle', 'rb') as handle:
    mean_gauss = pickle.load(handle)
with open(picklefolder + os.sep + 'sigma_gauss.pickle', 'rb') as handle:
    sigma_gauss = pickle.load(handle)

def pre_context( evList , i, win_length ):
    c = np.zeros(128)
    for j in range(i-1 , i-win_length-1, -1):
        if j < 0 or evList[j].pitches == -1:
            break
        else:
            if isinstance(evList[j].pitches, list):
                for p in evList[j].pitches:
                    a = 1/(sigma_gauss*np.sqrt(2)*math.pi)
                    x = evList[i].offset - evList[j].offset
                    y = a*np.exp( -(1/2)*np.power( (x-mean_gauss)/sigma_gauss , 2 ) )
                    c[ p ] += y
            else:
                p = evList[j].pitches
                a = 1/(sigma_gauss*np.sqrt(2)*math.pi)
                x = evList[i].offset - evList[j].offset
                y = a*np.exp( -(1/2)*np.power( (x-mean_gauss)/sigma_gauss , 2 ) )
                c[ p ] += y
    return c
# end pre_context
def post_context( evList , i, win_length ):
    c = np.zeros(128)
    for j in range(i+1 , i+win_length+1, 1):
        if j >= len(evList) or evList[j].pitches == -1:
            break
        else:
            if isinstance(evList[j].pitches, list):
                for p in evList[j].pitches:
                    a = 1/(sigma_gauss*np.sqrt(2)*math.pi)
                    x = evList[i].offset - evList[j].offset
                    y = a*np.exp( -(1/2)*np.power( (x-mean_gauss)/sigma_gauss , 2 ) )
                    c[ p ] += y
            else:
                p = evList[j].pitches
                a = 1/(sigma_gauss*np.sqrt(2)*math.pi)
                x = evList[i].offset - evList[j].offset
                y = a*np.exp( -(1/2)*np.power( (x-mean_gauss)/sigma_gauss , 2 ) )
                c[ p ] += y
    return c
# end post_context

with open(picklefolder + os.sep + 'events_list.pickle', 'rb') as handle:
    events_list = pickle.load(handle)

# keep chord names in a keys list and 24D context vectors
dkeys = []
dvalues = []
for i,ev in enumerate( events_list ):
    print('processing: ' + str( i ) + ' / ' + str(len(events_list)) )
    if ev.pitches != -1:
        if repr( ev.pitches ) not in dkeys:
            dkeys.append( repr( ev.pitches ) )
            # initialise context array and append to dvalues
            tmp_context = np.hstack( ( pre_context(events_list, i, w) , post_context(events_list, i, w) ) )
            dvalues.append( tmp_context )
        else:
            # find index of pitches
            tmp_idx = dkeys.index( repr( ev.pitches ) )
            # add context in proper location of d_values
            tmp_context = np.hstack( ( pre_context(events_list, i, w) , post_context(events_list, i, w) ) )
            dvalues[tmp_idx] = dvalues[tmp_idx] + tmp_context
# after all has been initialised, normalise to sum to 1
# and append in a single matrix
context_matrix = np.zeros( ( len(dvalues) , 256 ) )
for i, v in enumerate( dvalues ):
    if np.sum(v) > 0:
        dvalues[i] = v / np.sum(v)
        context_matrix[i,:] = dvalues[i]

with open(picklefolder + os.sep + 'dkeys.pickle', 'wb') as handle:
    pickle.dump(dkeys, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(picklefolder + os.sep + 'dvalues.pickle', 'wb') as handle:
    pickle.dump(dvalues, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(picklefolder + os.sep + 'context_matrix.pickle', 'wb') as handle:
    pickle.dump(context_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)