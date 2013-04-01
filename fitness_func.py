# Contains various fitness functions, note lists, etc needed to create and evalate
# songs by NEAT Composer

import mingus.core.diatonic as diatonic
from mingus.containers.Track import Track
from mingus.containers.Note import Note
from mingus.containers.Bar import Bar
from mingus.core import *


#List of diatonic notes in range of this program
diatonic_list = ['A-0','B-0','C-1','D-1','E-1','F-1','G-1']

#List of all notes NEAT Composer uses
note_list = ['A-0', 'A#-0', 'B-0', 'C-1', 'C#-1', 'D-1', 'D#-1', 'E-1', 'F-1', 'F#-1', 'G-1', 'G#-1', 'A-1', 'A#-1', 'B-1', 'C-2', 'C#-2', 'D-2', 'D#-2', 'E-2', 'F-2', 'F#-2', 'G-2', 'G#-2', 'A-2', 'A#-2', 'B-2', 'C-3', 'C#-3', 'D-3', 'D#-3', 'E-3', 'F-3', 'F#-3', 'G-3', 'G#-3', 'A-3', 'A#-3', 'B-3', 'C-4', 'C#-4', 'D-4', 'D#-4', 'E-4', 'F-4', 'F#-4', 'G-4', 'G#-4', 'A-4', 'A#-4', 'B-4', 'C-5', 'C#-5', 'D-5', 'D#-5', 'E-5', 'F-5', 'F#-5', 'G-5', 'G#-5', 'A-5', 'A#-5', 'B-5', 'C-6', 'C#-6', 'D-6', 'D#-6', 'E-6', 'F-6', 'F#-6', 'G-6', 'G#-6', 'A-6', 'A#-6', 'B-6', 'C-7', 'C#-7', 'D-7', 'D#-7', 'E-7', 'F-7', 'F#-7', 'G-7', 'G#-7', 'A-7', 'A#-7', 'B-7', 'C-8']

#uses a smaller note range to reduce search space and make things easier for early stages
restricted_note_list = ['C-4', 'C#-4', 'D-4', 'D#-4', 'E-4', 'F-4', 'F#-4', 'G-4', 'G#-4', 'A-4', 'A#-4', 'B-4', 'C-5', 'C#-5', 'D-5', 'D#-5', 'E-5', 'F-5', 'F#-5', 'G-5', 'G#-5', 'A-5', 'A#-5', 'B-5', 'C-6']


a_Major = ['A-0', 'B-0', 'C#-1', 'D-1', 'E-1', 'F#-1', 'G#-1']
b_Major = ['A#-0', 'B-0', 'C#-1', 'D#-1', 'E-1', 'F#-1', 'G#-1']
c_Major = diatonic_list
d_Major = ['A-0', 'B-0', 'C#-1','D-1', 'E-1', 'F#-1', 'G-1']
e_Major = ['A-0', 'B-0', 'C#-1', 'D#-1', 'E-1', 'F#-1', 'G#-1']
f_Major = ['A-0', 'A#-0', 'C-1', 'D-1', 'E-1', 'F-1', 'G-1']
g_Major = ['A-0', 'A#-0', 'C-1', 'D-1', 'E-1', 'F#-1','G-1'] #get rest by shifting up 12

key_dict = {"A": a_Major, "B": b_Major, "C": c_Major, "D": d_Major, "E": e_Major, "F": f_Major, "G":g_Major}
#Dictionary of all fitness functions, making it easier to call them

#Seems to have upper bound of about 0.85 for popsize = 100
def is_diatonic(a_song, *args):  #Checks to see if all notes are diatonic (no # or b)
  matches = 0
  fitness = 0
  length = int(a_song.length)
  for x in range(0, length):
    note = a_song.song[x/4][x%4][2][0]
    for y in (diatonic_list):
      if(int(Note(note))%12 == int(Note(y))%12):
        matches = matches+1
  
  a_song.fitness = matches / a_song.length
  return a_song.fitness

#Upper bound of 0.6ish for popsize = 100
def in_key(a_song, *args):  #Checks to see if all notes fall within a certain range
  matches = 0
  key = args[0]
  length = int(a_song.length)
  for x in range(0, length):
    note = a_song.song[x/4][x%4][2][0]
    for y in key_dict[key]:
      if(int(Note(note))%12 == int(Note(y))%12):
        matches = matches+1

  a_song.fitness = matches/a_song.length
  return a_song.fitness


def fitness_range(a_song, *args):
  upper = 0
  lower = 99
  target = args[1]
  fitness = 0
  for x in range(0, int(song.length)):
    note = Note(a_song.song[x/4][x%4][2][0])
    if(int(note) > upper):
      upper = int(note)
    if(int(note) < lower):
      lower = int(note)
  note_range = upper-lower
  if(note_range <= target):
    return note_range
  
  return note_range - target

def fitness_var(a_song, *args):
  target = args[2]
  avg = 0
  var = 0
  for x in range(0, int(song.length)):
    note = Note(a_song.song[x/4][x%4][2][0])
    avg = avg + int(note)

  for y in range(0, int(song.length)):
    note = Note(a_song.song[y/4][y%4][2][0])
    var = int(note)**2 - avg**2
  var = var/(int(song.length)-1)
  
  

def fitness_note(a_song, *args):
  fitness = 0
  target = args[3]
  for x in range(0, int(song.length)):
    note = Note(a_song.song[x/4][x%4][2][0])
    if(note == Note(target)):
      fitness = fitness + 1
  return fitness/song.length 

 

functions = {"diatonic": is_diatonic, "in_key": in_key}

funct = [is_diatonic, in_key, fitness_range, fitness_var, fitness_note]

