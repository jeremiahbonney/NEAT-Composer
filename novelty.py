# Contains the novelty search functions as well as the general novelty search function, 
# which calculates how far apart each of the songs are from each other in respect to the novelty params.


from mingus.containers.Note import Note
from mingus.containers.Track import Track
from mingus.containers.Bar import Bar

#Novelty parameters used for novelty search

def song_slope(song):  #Takes sum of slopes between notes
  fitness = 0
  for x in range(0, int(song.length) -1):
    note = Note(song.song[x/4][x%4][2][0])
    note2 = Note(song.song[x/4][x%4][2][0])
    fitness = int(note2) - int(note)
  print "fitness song slope is", fitness
  return fitness


def song_range(song):
  lower = 100000000
  upper = -10000000000
  for x in range(0, int(song.length) -1):
    note = Note(song.song[x/4][x%4][2][0])
    if(int(note) > upper):
      upper = int(note)
    if(int(note) < lower):
      lower = int(note)
  print "fitness song range is", upper-lower
  return upper - lower

def variance(song):
  note_avg = 0
  var = 0
  for x in range(0, int(song.length)-1):
    note_avg += int(song.song[x/4][x%4][2][0])
  note_avg = note_avg / (int(song.length))
  for y in range(0, int(song.length)-1):
    var = var + (int(song.song[x/4][x%4][2][0]) - note_avg)**2
  print "fitness var is", var/song.length #12 is population size
  return var/song.length
    
novelty_func = [song_slope, song_range, variance]

def set_novelty_params(song_list):
  for song in song_list:
    song.novelty_params = []
    for function in novelty_func:
      song.novelty_params.append(function(song))

#Finds novelty distance between two songs, assumes the params are in 
#an array in the song object
def novelty_dist(song1, song2): 
  dist = 0
  for x in range(0,len(song1.novelty_params)):
    dist = dist + (song2.novelty_params[x] - song1.novelty_params[x])**2

  return (dist**0.5)


#Sets novelty_score of every song in song_list. Does NOT set it as fitness 
#So caller must do this themselves if necessary
def novelty_search(song_list):
  dist_list = []
  x = 0
  for song1 in song_list:
    for song2 in song_list:
      if(song1 == song2):
        continue
      dist_list.append(novelty_dist(song1, song2))
    dist_list.sort()
    song1.novelty_score = (sum(dist_list[0:9])/10) #Gets avg of 10 nearest distances
    print song1.novelty_score, "novelty score of ", x
    dist_list = []
    x = x+1
  print "\n"
  return
