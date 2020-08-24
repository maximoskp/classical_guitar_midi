# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:04:01 2020

@author: maximos
"""

import music21 as m21
import os
import pickle
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# foldername = 'midifiles'
# foldername = 'guitar_classclef'
foldername = 'allfiles'
# foldername = 'testfiles'
picklefolder = 'pickles' + os.sep + 'data_as_a_sequence'

total_files = 0
single_guitar_files = 0

events_list = []
pitch_events_list = []

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

for i,f in enumerate( os.listdir(foldername) ):
    if f.endswith('.mid') or f.endswith('.midi'):
        print( '------------------------------------------------------' )
        print(str(i+1) + '/' + str(len(os.listdir(foldername))) + ' - processing file: ' + f)
        try:
            s = m21.converter.parse( foldername + os.sep + f )
            total_files += 1
            if len( s.parts ) == 1:
                print('single guitar');
                single_guitar_files += 1
                p = s.parts[0]
                fl = p.flat.notes
                # make start event
                tmp_event = MusicEvent( 'start' )
                events_list.append( tmp_event )
                pitch_events_list.append( repr( tmp_event.pitches ) )
                for f in fl:
                    tmp_event = MusicEvent( f )
                    events_list.append( tmp_event )
                    pitch_events_list.append( repr( tmp_event.pitches ) )
                    
            else:
                print('multiple guitars');
            print('ok!')
            print('single_guitar_files: ' + str( single_guitar_files ) )
            print('single-to-total ratio: ' + str( single_guitar_files/total_files ) )
        except:
            print('FAILED')

# keep counter
pitches_counter = Counter( pitch_events_list )
# and plot
labels, values = zip(*pitches_counter.items())
indexes = np.arange(len(labels))
plt.clf()
plt.bar(indexes, values)
plt.savefig('figs' + os.sep + 'pitches_whole_data_distribution.png', dpi=600)
# and plot

with open(picklefolder + os.sep + 'events_list.pickle', 'wb') as handle:
    pickle.dump(events_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'pitch_events_list.pickle', 'wb') as handle:
    pickle.dump(pitch_events_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

