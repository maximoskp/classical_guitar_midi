# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:21:44 2020

@author: maximos
"""

import music21 as m21
import os
import pickle
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# foldername = 'midifiles'
foldername = 'guitar_classclef'
# foldername = 'testfiles'
picklefolder = 'pickles' + os.sep + 'single_guitar_stats'

single_guitar_files = 0

note_events_number = 0
note_events = []

chord_events_number = 0
chord_events = []

rest_events_number = 0
rest_events = []

other_events_number = 0
other_events = []

total_files = 0

class NoteEvent:
    def __init__(self, m21_note):
        self.pitch = m21_note.pitch.midi
        self.offset_category = self.compute_offset_category( m21_note.offset )
        self.duration = self.compute_duration_category( float( m21_note.duration.quarterLength ) )
        self.velocity = self.compute_velocity_category( float( m21_note.volume.velocity ) )
    # end constructor
    
    def compute_offset_category(self, x):
        return float(x) - int(x)
    # end compute_offset_category
    def compute_duration_category(self, x):
        # quantise to 1/N
        N = 128
        x = int( N * float(x))/N
        return float(x) - int(x)
    # end compute_duration_category
    def compute_velocity_category(self, x):
        # quantise to 1/N
        N = 10
        x = int( N * float(x))/N
        return float(x) - int(x)
    # end compute_duration_category
# end NoteEvent class
class ChordEvent:
    def __init__(self, m21_note):
        self.pitches = [p.midi for p in m21_note.pitches]
        self.offset_category = self.compute_offset_category( m21_note.offset )
        self.duration = self.compute_duration_category( float( m21_note.duration.quarterLength ) )
        self.velocity = self.compute_velocity_category( float( m21_note.volume.velocity ) )
    # end constructor
    
    def compute_offset_category(self, x):
        return float(x) - int(x)
    # end compute_offset_category
    def compute_duration_category(self, x):
        # quantise to 1/N
        N = 128
        x = int( N * float(x))/N
        return float(x) - int(x)
    # end compute_duration_category
    def compute_velocity_category(self, x):
        # quantise to 1/N
        N = 10
        x = int( N * float(x))/N
        return float(x) - int(x)
    # end compute_duration_category
# end ChordEvent class
class MusicEvent:
    def __init__(self, m21_note):
        if m21_note.isChord:
            self.pitches = [p.midi for p in m21_note.pitches]
        elif m21_note.isNote:
            self.pitch = m21_note.pitch.midi
        self.offset = float( m21_note.offset )
        self.duration = float( m21_note.duration.quarterLength )
        self.velocity = float( m21_note.volume.velocity )
    # end constructor
# end ChordEvent class

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
                for f in fl:
                    if f.isNote:
                        note_events_number += 1
                        tmp_note_event = NoteEvent( f )
                        note_events.append( tmp_note_event )
                    elif f.isChord:
                        tmp_chord_event = ChordEvent( f )
                        chord_events_number += 1
                        chord_events.append( tmp_chord_event )
                    elif f.isRest:
                        rest_events_number += 1
                        rest_events.append( f )
                    else:
                        other_events_number += 1
                        other_events.append( f )
            else:
                print('multiple guitars');
            print('ok!')
            print('single_guitar_files: ' + str( single_guitar_files ) )
            print('single-to-total ratio: ' + str( single_guitar_files/total_files ) )
            print( 'note_events_number: ' + str( note_events_number ) )
            print( 'chord_events_number: ' + str( chord_events_number ) )
            print( 'rest_events_number: ' + str( rest_events_number ) )
            print( 'other_events_number: ' + str( other_events_number ) )
        except:
            print('FAILED')


note_pitches = []
unique_note_pitches = []
unique_note_events = []
note_lowest_pitch = 127
note_highest_pitch = 0
print('finding unique notes')
for i, n in enumerate( note_events ):
    print( 'notes: ' + str(i) + '/' + str( len(note_events) ) )
    print( 'unique note events so far: ' + str( len(unique_note_events) ) )
    print( 'unique note pitches so far: ' + str( len(unique_note_pitches) ) )
    note_pitches.append( n.pitch )
    if note_lowest_pitch > n.pitch:
        note_lowest_pitch = n.pitch
    if note_highest_pitch < n.pitch:
        note_highest_pitch = n.pitch
    if n.pitch not in unique_note_pitches:
        unique_note_pitches.append( n.pitch )
    # if n not in unique_note_events:
        # unique_note_events.append( n )

chord_pitches = []
unique_chord_pitches = []
unique_chord_events = []
chord_lowest_pitch = 127
chord_highest_pitch = 0
print('finding unique chords')
for i,n in enumerate( chord_events ):
    print( 'chords: ' + str(i) + '/' + str( len(chord_events) ) )
    print( 'unique chord events so far: ' + str( len(unique_chord_events) ) )
    print( 'unique chord pitches so far: ' + str( len(unique_chord_pitches) ) )
    m = []
    for pp in n.pitches:
        m.append( pp )
        if chord_lowest_pitch > pp:
            chord_lowest_pitch = pp
        if chord_highest_pitch < pp:
            chord_highest_pitch = pp
    m.sort()
    chord_pitches.append( repr(m) )
    if repr( m ) not in unique_chord_pitches:
        unique_chord_pitches.append( repr(m) )
    # if n not in unique_chord_events:
        # unique_chord_events.append( n )

unique_rest_events = []
for n in rest_events:
    if n not in unique_rest_events:
        unique_rest_events.append( n )

unique_note_pitches.sort()
unique_chord_pitches.sort()

print('ok!')
print('single_guitar_files: ' + str( single_guitar_files ) )
print('single-to-total ratio: ' + str( single_guitar_files/total_files ) )
print( 'note_events_number: ' + str( note_events_number ) )
print( 'chord_events_number: ' + str( chord_events_number ) )
print( 'rest_events_number: ' + str( rest_events_number ) )
print( 'other_events_number: ' + str( other_events_number ) )
print( 'unique_note_events number: ' + str( len( unique_note_events ) ) )
print( 'unique_chord_events number: ' + str( len( unique_chord_events ) ) )
print( 'unique_rest_events number: ' + str( len( unique_rest_events ) ) )
print( 'unique_note_pitches number: ' + str( len( unique_note_pitches ) ) )
print( 'unique_chord_pitches number: ' + str( len( unique_chord_pitches ) ) )
print( 'lowest note pitch: ' + str( note_lowest_pitch ) )
print( 'highest note pitch: ' + str( note_highest_pitch ) )
print( 'lowest chord pitch: ' + str( chord_lowest_pitch ) )
print( 'highest chord pitch: ' + str( chord_highest_pitch ) )

with open('single_guitar_stats.txt', 'w') as f:
    f.write('single_guitar_files: ' + str( single_guitar_files ) + '\n' )
    f.write('total_files: ' + str( total_files ) + '\n' )
    f.write('single-to-total ratio: ' + str( single_guitar_files/total_files ) + '\n' )
    f.write( 'note_events_number: ' + str( note_events_number ) + '\n' )
    f.write( 'chord_events_number: ' + str( chord_events_number ) + '\n' )
    f.write( 'rest_events_number: ' + str( rest_events_number ) + '\n' )
    f.write( 'other_events_number: ' + str( other_events_number ) + '\n' )
    f.write( 'unique_note_events number: ' + str( len( unique_note_events ) ) + '\n' )
    f.write( 'unique_chord_events number: ' + str( len( unique_chord_events ) ) + '\n' )
    f.write( 'unique_rest_events number: ' + str( len( unique_rest_events ) ) + '\n' )
    f.write( 'unique_note_pitches number: ' + str( len( unique_note_pitches ) ) + '\n'  )
    f.write( 'unique_chord_pitches number: ' + str( len( unique_chord_pitches ) ) + '\n'  )
    f.write( 'lowest note pitch: ' + str( note_lowest_pitch ) + '\n'  )
    f.write( 'highest note pitch: ' + str( note_highest_pitch ) + '\n'  )
    f.write( 'lowest chord pitch: ' + str( chord_lowest_pitch ) + '\n'  )
    f.write( 'highest chord pitch: ' + str( chord_highest_pitch ) + '\n'  )
    f.close()

# keep counter
note_pitches_counter = Counter(note_pitches)
chord_pitches_counter = Counter(chord_pitches)
# and plot
labels, values = zip(*note_pitches_counter.items())
indexes = np.arange(len(labels))
plt.clf()
plt.bar(indexes, values)
plt.savefig('figs' + os.sep + 'notes_distribution.png', dpi=300)
# and plot
labels, values = zip(*chord_pitches_counter.items())
indexes = np.arange(len(labels))
plt.clf()
plt.bar(indexes, values)
plt.savefig('figs' + os.sep + 'chords_distribution.png', dpi=300)

with open(picklefolder + os.sep + 'note_events.pickle', 'wb') as handle:
    pickle.dump(note_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'chord_events.pickle', 'wb') as handle:
    pickle.dump(chord_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'rest_events.pickle', 'wb') as handle:
    pickle.dump(rest_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'other_events.pickle', 'wb') as handle:
    pickle.dump(other_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'unique_note_events.pickle', 'wb') as handle:
    pickle.dump(unique_note_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'unique_chord_events.pickle', 'wb') as handle:
    pickle.dump(unique_chord_events, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'unique_note_pitches.pickle', 'wb') as handle:
    pickle.dump(unique_note_pitches, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'chord_pitches.pickle', 'wb') as handle:
    pickle.dump(chord_pitches, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'note_pitches.pickle', 'wb') as handle:
    pickle.dump(note_pitches, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'unique_chord_pitches.pickle', 'wb') as handle:
    pickle.dump(unique_chord_pitches, handle, protocol=pickle.HIGHEST_PROTOCOL)