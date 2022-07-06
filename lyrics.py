#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 19:04:05 2022

@author: mobeets
"""
import glob
import json
import os.path

#%%

def to_json(data, outfile):
    with open(outfile, 'w') as f:
        json.dump(data, f)

def usdb_to_json(infile):
    with open(infile) as f:
        lines = f.readlines()
    if not lines:
        return
    
    get_line = lambda key: [x for x in lines if x.startswith('#{}'.format(key.upper()))][0].split('#{}:'.format(key.upper()))[1].strip()
    artist = get_line('artist')
    title = get_line('title')
    bpm = float(get_line('bpm').replace(',', '.'))
    gap = int(get_line('gap'))
    note_start_keys = [':', '*', 'F']
    notes = []
    for line in lines:
        if any([line.startswith(key) for key in note_start_keys]):
            item = line.split()
            t = int(item[1])
            dur = int(item[2])
            pitch = int(item[3])
            word = item[4].strip()
            word = word.replace('~', '')
            note = {'time': t, 'duration': dur, 'note': pitch, 'name': word}
            notes.append(note)
    # to do:
    # - default ticks per beat is 4?
    # - default offset of notes is 60?
    return {'artist': artist, 'title': title,
            'bpm': bpm, 'gap': gap, 'notes': notes,
            'ticks_per_beat': 4, 'note_transpose': 60}
    
#%%

infiles = glob.glob('usdb/*.txt')
for infile in infiles:
    outfile = os.path.join('notes', os.path.split(infile)[1].replace('.txt', '.json'))
    print(infile, outfile)
    song = usdb_to_json(infile)
    to_json(song, outfile)

#%%

outfile = 'songs.json'
songs = []
notefiles = glob.glob('notes/*.json') + glob.glob('mp3/*.mp3')
for notefile in notefiles:
    key = os.path.splitext(os.path.split(notefile)[1])[0]
    fnote = os.path.join('notes', key + '.json')
    snote = os.path.join('mp3', key + '.mp3')
    if os.path.exists(fnote) and os.path.exists(snote):
        songs.append(key)
    else:
        print("Missing mp3 or json for file: {}".format(key))
songs = list(set(songs))
songs = [{key: key} for key in songs]
to_json(songs, outfile)
