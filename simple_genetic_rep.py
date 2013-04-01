#This is a text based version of NEAT Composer which was the beta before creating the UI version, which has more features.

#from mingus.midi import fluidsynth
#from mingus.containers.Note import Note
#from mingus.containers.Bar import Bar
import random
import sys


pop_created = 0
population = []
notes = list("ABCDEFG")
runprogram = 1
#fluidsynth.init("FluidR3_GM.sf2")


def create_population():
  song = ""
  for y in range(0, 8):
    for z in range(0, 8):
      whichnote = random.randint(0,6)
      song += notes[whichnote]
    population.append(song)
    song = ""
  return

#def play_song(song):
 # mingus_song = Bar()
 # mingus_song.set_meter((8,4))
 # for number in range(0,7):
 #   individual_notes = str(song)
 #   for note in individual_notes:
 #     mingus_song.place_notes(note, 4)
 # fluidsynth.play_Bar(mingus_song, 1, 150)
 # return
  
def mutation(x):
  global notes
  whatbeat = random.randint(0,7)
  whichnote = random.randint(0,6)
  mutatedsong = list(x)
  mutatedsong[whatbeat] = notes[whichnote]
  print "note", whatbeat+1, "mutated to", notes[whichnote]
  return "".join(mutatedsong)
  
def print_pop():
  num = 1
  while (num < 9):
    print num, population[num-1], "\n"
    num = num+1
  
def main():
  global population
  global pop_created
  while (runprogram == 1):
    choice = raw_input("Please choose one of the following\n1) Display population\n2) Mutate a member of the population\n3) Copy one member of the population over the others\n4) Play a song\n5) Quit the program\n")
    if(choice == "1"):
      if(pop_created == 0):
        print "Creating population"
        create_population()
        pop_created = 1
      print_pop()
    elif(choice == "2"):
      song_to_mutate = int(raw_input("Which song would you like to mutate?\n"))
      population[song_to_mutate-1] =  mutation(population[song_to_mutate-1])
      print "Printing new population\n"
      print_pop()
    elif(choice == "3"):
      song_to_copy = int(raw_input("Which song would you like to fill the population with?\n"))
      for x in range(0,8):
        if (song_to_copy -1 == x ):
          pass
        else:
          population[x] = population[song_to_copy -1]
      print "Printing new population\n"
      print_pop()
    elif(choice == "4"):
      song_choice = int(raw_input("Which song would you like to play?\n"));
      play_song(population[song_choice -1])
    elif(choice == "5"):
      sys.exit("Program exited")
    else:
      print "That is not a valid choice, please choose again"

  
main()
