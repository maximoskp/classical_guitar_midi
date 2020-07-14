# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 07:28:39 2020

@author: user
"""


import music21 as m21
import os

def getChordsRestRepresentations(foldername, filename):
    try:
        s = m21.converter.parse( foldername + os.sep + filename )
        # for each part
        f_parts = []
        c_parts = []
        # string representations
        r_parts = []
        for p in s.parts:
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
                    r.append( repr( m ) )
            r_parts.append(r)
    except:
        r_parts = []
    return r_parts