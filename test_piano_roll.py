# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 09:14:31 2021

@author: user
"""

import music21 as m21
import os
from pitchscapes.reader import piano_roll
from pitchscapes.reader import read_midi_mido
from pitchscapes.reader import read
from pitchscapes.reader import chordify
import mido

import matplotlib.pyplot as plt

from my_midi_tools import my_piano_roll
from my_midi_tools import my_chordify

# TODOs:
# GJT piano in -> guitar out
# style transfer

# %% 

folder = 'midifiles'
pieces = os.listdir(folder)

# %% 

# s = m21.converter.parse( os.path.join(folder, pieces[0]) )


# %% 

# f = s.plot()

# %% 

# f = piano_roll( os.path.join(folder, pieces[0]))

# %% 

# m = mido.MidiFile( os.path.join(folder, pieces[0]) )

# %% get min max pitches in dataset

from my_midi_tools import my_chordify
# get min and max pitch
general_min = 128
general_max = -1
for idx in range( len(pieces) ):
    print(pieces[idx])
    # m = read_midi_mido( os.path.join(folder, pieces[idx]) )
    m = read( os.path.join(folder, pieces[idx]) )
    duration_events, onset_events = my_chordify(m)
    for e in duration_events:
        for p in e.data:
            if general_max < p:
                general_max = p
            if general_min > p:
                general_min = p



# %% 

m = read_midi_mido( os.path.join(folder, pieces[idx]) )
duration_events, onset_events = my_chordify(m)

# n, d = my_piano_roll(c, return_durations=True)
x_dur = my_piano_roll(duration_events, min_pitch=24, max_pitch=120, return_durations=False)
x_ons = my_piano_roll(onset_events, min_pitch=24, max_pitch=120, return_durations=False)

x = x_dur.astype('float32') + 2*x_ons.astype('float32')

plt.imshow(x.T, origin='lower', cmap='gray_r')

# %% 

for time_idx, event in enumerate(duration_events):
    print(str(time_idx) + ' - ' + repr(event.time) + ' : ' + repr(event.data) )