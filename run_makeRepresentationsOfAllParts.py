# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 08:01:21 2020

@author: user
"""


from collections import Counter
import splitFileInParts as sfp
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle

foldername = 'midifiles'
# foldername = 'testfiles'
picklefolder = 'pickles'

r_parts = []
files_not_parsed = []
invalid_parts = []
'''
Giuliani_Papillon_Op50_No1.mid
Giuliani_Papillon_Op50_No12.mid
Giuliani_Papillon_Op50_No13.mid
Pernambuco_Brasileirinho.mid
'''

for i,f in enumerate( os.listdir(foldername) ):
    if f.endswith('.mid') or f.endswith('.midi'):
        print(str(i) + '/' + str(len(os.listdir(foldername))) + ' - processing file: ' + f)
        s, val_status, p_idx = sfp.getChordsRestRepresentations(foldername, f)
        if len(s) > 0:
            for i in range(len(s)):
                if val_status[i] == 'valid':
                    r_parts.append( s[i] )
                else:
                    invalid_parts.append( {'file': f, 'reason': val_status[i]} )
        else:
            files_not_parsed.append(f)

# make counter for all parts
cnt = []
for i,r in enumerate( r_parts ):
    if i == 0:
        cnt = Counter( r )
    else:
        cnt = cnt + Counter( r )

# sort by value
s_cnt = sorted(cnt.items(), key=lambda pair: pair[1], reverse=True)

# preparee for plotting
# labels, values = zip(*s_cnt.items())
labels = []
values = []
for s in s_cnt:
    labels.append( s[0] )
    values.append( s[1] )

indexes = np.arange(len(labels))
width = 1

plt.bar(indexes, values, width)
# plt.xticks(indexes + width * 0.5, labels)
plt.savefig('histogram.png', dpi=300)

with open(picklefolder + os.sep + 'r_parts.pickle', 'wb') as handle:
    pickle.dump(r_parts, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 's_cnt.pickle', 'wb') as handle:
    pickle.dump(s_cnt, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'files_not_parsed.pickle', 'wb') as handle:
    pickle.dump(files_not_parsed, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(picklefolder + os.sep + 'invalid_parts.pickle', 'wb') as handle:
    pickle.dump(invalid_parts, handle, protocol=pickle.HIGHEST_PROTOCOL)


'''
with open(picklefolder + os.sep + 'r_parts.pickle', 'rb') as handle:
    r_parts_new = pickle.load(handle)

with open(picklefolder + os.sep + 's_cnt.pickle', 'rb') as handle:
    s_cnt_new = pickle.load(handle)
'''