# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 07:28:39 2020

@author: user
"""


import music21 as m21
import os
# C:\Program Files\MuseScore 3\bin
env = m21.environment.UserSettings()
env['musicxmlPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
env['midiPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
env['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'

'''
Standard guitar tuning for a six string is
E3/68 - B2/63 - G2/59 - D2/54 - A1/49 - E1/44
'''


def getChordsRestRepresentations(foldername, filename):
    highest_pitch = 92 # 24th fret
    lowest_pitch = 36 # dropped C
    validation_statuses = []
    try:
        s = m21.converter.parse( foldername + os.sep + filename )
        # for each part
        f_parts = []
        c_parts = []
        # string representations
        r_parts = []
        part_idxs = []
        for p_idx, p in enumerate( s.parts ):
            # keep if part is valid or describe invalidity cause
            validation_status = 'valid'
            # flatten
            f = p.flat.notes
            f_parts.append(f)
            # chordify
            c = f.chordify()
            c_parts.append(c)
            # string representation
            r = []
            for ch in c:
                if ch.isRest:
                    r.append('r')
                else:
                    m = [ptch.midi for ptch in ch.pitches]
                    # check if part includes only pitches in the permitted range
                    # and if part has at most 6 voices
                    if max(m) > highest_pitch:
                        print('highest violated: ' + filename + ' - part: ' + str(p_idx) + ' - ' + repr(m))
                        validation_status = 'highest_invalidation' + '-part: ' + str(p_idx)
                    elif min(m) < lowest_pitch:
                        print('lowest violated: ' + filename + ' - part: ' + str(p_idx) + ' - ' + repr(m))
                        validation_status = 'lowest_invalidation' + '-part: ' + str(p_idx)
                    elif len(m) > 6:
                        print('more than 6 notes: ' + filename + ' - part: ' + str(p_idx) + ' - ' + repr(m))
                        validation_status = 'voices_num_invalidation' + '-part: ' + str(p_idx)
            r_parts.append(r)
            validation_statuses.append(validation_status)
    except:
        r_parts = []
        validation_status = 'could_not_parse'
        validation_statuses.append(validation_status)
        part_idxs = []
    return r_parts, validation_statuses, part_idxs