#Contains various fitness functions, note lists, etc needed to create and evalate
#songs by NEAT Composer


import mingus.core.diatonic as diatonic
from mingus.containers.Track import Track
from mingus.containers.Note import Note
from mingus.containers.Bar import Bar
from mingus.core import *


#List of diatonic notes in range of this program
diatonic_list = ['A-0','B-0','C-1','D-1','E-1','F-1','G-1','A-1','B-1','C-2','D-2','E-2','F-2','G-2','A-2','B-2','C-3','D-3','E-3','F-3','G-3','A-3','B-3','C-4','D-4','E-4','F-4','G-4','A-4','B-4','C-5','D-5','E-5','F-5','G-5','A-5','B-5','C-6','D-6','E-6','F-6','G-6','A-6','B-6','C-7','D-7','E-7','F-7','G-7','A-7','B-7','C-8']

#List of all notes NEAT Composer uses
note_list = ['A-0', 'A#-0', 'B-0', 'C-1', 'C#-1', 'D-1', 'D#-1', 'E-1', 'F-1', 'F#-1', 'G-1', 'G#-1', 'A-1', 'A#-1', 'B-1', 'C-2', 'C#-2', 'D-2', 'D#-2', 'E-2', 'F-2', 'F#-2', 'G-2', 'G#-2', 'A-2', 'A#-2', 'B-2', 'C-3', 'C#-3', 'D-3', 'D#-3', 'E-3', 'F-3', 'F#-3', 'G-3', 'G#-3', 'A-3', 'A#-3', 'B-3', 'C-4', 'C#-4', 'D-4', 'D#-4', 'E-4', 'F-4', 'F#-4', 'G-4', 'G#-4', 'A-4', 'A#-4', 'B-4', 'C-5', 'C#-5', 'D-5', 'D#-5', 'E-5', 'F-5', 'F#-5', 'G-5', 'G#-5', 'A-5', 'A#-5', 'B-5', 'C-6', 'C#-6', 'D-6', 'D#-6', 'E-6', 'F-6', 'F#-6', 'G-6', 'G#-6', 'A-6', 'A#-6', 'B-6', 'C-7', 'C#-7', 'D-7', 'D#-7', 'E-7', 'F-7', 'F#-7', 'G-7', 'G#-7', 'A-7', 'A#-7', 'B-7', 'C-8']



#Dictionary of all fitness functions, making it easier to call them

#Seems to have upper bound of about 0.85 for popsize = 100
def is_diatonic(a_song, *args):  #Checks to see if all notes are diatonic (no # or b)
  sum = 0
  fitness = 0
  length = int(a_song.length)
  for x in range(0, length):
    note = a_song.song[x/4][x%4][2][0]
    for y in (diatonic_list):
      if(note == Note(y)):
        sum = sum+1
  
  a_song.fitness = sum / a_song.length
  return a_song.fitness

#Upper bound of 0.6ish for popsize = 100
def in_range(a_song, *args):  #Checks to see if all notes fall within a certain range
  sum = 0
  lower = args[0]
  upper = args[1]
  length = int(a_song.length)
  for x in range(0, length):
    note = a_song.song[x/4][x%4][2][0]
    if(note >= lower) and (note <= upper):
      sum = sum+1
  a_song.fitness = sum/a_song.length
  return a_song.fitness

functions = {"diatonic": is_diatonic, "in_range": in_range}

