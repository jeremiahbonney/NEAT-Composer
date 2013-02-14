#NEAT Composer text version. This version uses OOP to make it cleaner 
#and hopefully make transfering to a GUI easier. Also puts fitness
#functions and other messy stuff in the fitness_func.py file.

import MultiNEAT as NEAT
#from mingus.midi import fluidsynth   Commented out until they work on lab machines
#from mingus.midi import MidiFileOut
from mingus.containers.Track import Track
from mingus.containers.Bar import Bar
from mingus.containers.Note import Note
from mingus.core import *
import random
import sys
import fitness_func  #contains fitness functions and other useful stuff

LENGTH = 8.0 #Global var for song length
GEN_NUM = 0
#Song class that keeps all the information about the song in one place, including
#the track itself, it's fitness, what generation it belongs to, it's length, etc
params = NEAT.Parameters()
params.PopulationSize = 100

params.DynamicCompatibility = True
params.CompatTreshold = 2.0
params.YoungAgeTreshold = 15
params.SpeciesMaxStagnation = 100
params.OldAgeTreshold = 35
params.MinSpecies = 5
params.MaxSpecies = 25
params.RouletteWheelSelection = False
params.RecurrentProb = 0
params.OverallMutationRate = 0.33

params.MutateWeightsProb = 0.90

params.WeightMutationMaxPower = 5.0
params.WeightReplacementMaxPower = 5.0
params.MutateWeightsSevereProb = 0.5
params.WeightMutationRate = 0.75
params.MaxWeight = 20

params.MutateAddNeuronProb = 0.01
params.MutateAddLinkProb = 0.05
params.MutateRemLinkProb = 0.05

rng = NEAT.RNG()
#rng.TimeSeed()
rng.Seed(0)



genome = NEAT.Genome(0,2,0,7,False,NEAT.ActivationFunction.UNSIGNED_SIGMOID,NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, params)



class Song:

  song = Track()
  fitness = 0
  gen_num = 0
  leader = False
  length = 0.0
  song_id = 0
  bpm = 150

  def __init__(self, genome, gen_num, song_id, length): #Global var for song length, song_id):
  
    self.genome = genome
    self.gen_num = gen_num 
    self.song_id = song_id
    self.length = length

  def gen_song(self): #Generates the notes by activating the network with various inputs
 		      #representing time and beat of measure from 0-1
    net = NEAT.NeuralNetwork()
    self.genome.BuildPhenotype(net)
    time = 0.0
    beat = 0.25
    track = Track()

    while(time <= 0.999999999):
      net.Input([time, beat])
      net.Activate()
      output = net.Output()[0]*88
      track + fitness_func.note_list[int(output)]
      beat = (beat+0.25)%1
      time = time + (1.0/self.length)
    self.song = track
    return

  def print_song(self): #Prints the song id and the notes (add duration too?)
    print self.song_id
    for x in range(0,(int)(self.length/4)):
      for num in range(0,4): print(self.song[x][num][2][0]),
    
    print
    return

  def play_song(self):  #Plays the song at 150 BPM using fluidsynth(make BPM a var later?)
 #   fluidsynth.play_Track(self.song, 1, 150)
    return

  def export_song(self, filename):
   # MidiFileOut.write_Track(filename, self.song, self.bpm, 0)
    pass
    
#End of Song Class


def evaluate(a_song, fitness_func):      #Takes a song and fitness function, then evaluates
  a_song.fitness = fitness_func(a_song)	 #the song via that fitness function. Also sets the
  return 				         #song_fitness attribute



def main():
  global GEN_NUM
  #creates default NEAT Genome
  
  
  population = NEAT.Population(genome, params, True, 1.0)
  genome_list = NEAT.GetGenomeList(population)
  song_list = []
  x = 1
  GEN_NUM = GEN_NUM + 1
  for genomes in genome_list: #goes through every genome, puts it in a Song object
                             #and adds that to a list making up the population
    c = Song(genomes, GEN_NUM, x, LENGTH)
    song_list.append(c)
    song_list[x-1].gen_song()
    x = x+1

#Main program loop
  while(1):
    choice = raw_input("Choose one of the following\n1) Print population\n2) Eval pop with fitness function\n3) Manually assign fitness\n4) Print fitness of POP\n5) Play a song\n6) Advance to next Generation\n7) Export song to midi file\n8)  Exit\n")
  
    if(choice == "1"): #Goes through and prints all songs
      for song in song_list:
        song.print_song()

    elif(choice == "2"): #User picks a fitness function and all songs are evaluated 
  		     #using that fitness function. Can happen for many generations
      func_choice = raw_input("Select fitness function: diatonic, or in_range\n")
      for song in song_list:
        evaluate(song, (fitness_func.functions[func_choice]))
        #genome[x].SetFitness(song.fitness) #Just in case I need to go back to the actual
					 #genome thing, since I think that's what's used
					 #by popEpoch

      for genomes in genome_list:
        genomes.SetFitness(song.fitness)

    elif(choice == "3"): #Pick a song out of the population and change it's fitness
      song_choice = raw_input("Which song's fitness would you like to change?\n")
      new_fit = raw_input("Enter new fitness\n")
      old_fit = song_list[(int)(song_choice)-1].fitness
      song_list[(int)(song_choice)-1].fitness = new_fit
      print "Song", song_choice, "fitness changed from", old_fit, "to", new_fit, "\n"

    elif(choice == "4"):
      for song in song_list:
        print "Song", song.song_id , "has fitness", song.fitness

    elif(choice == "5"): #Gets user choice of song and plays it
      song_choice = (int)(raw_input("Which song would you like to play?\n"))
      song_list[song_choice-1].play_song()
  
    elif(choice == "6"): #Advances to next generation and gets new population/songs
      population.Epoch()
      song_list = []
      genome_list = NEAT.GetGenomeList(population)
      x = 1
      GEN_NUM = GEN_NUM + 1
      for genomes in genome_list:
        c = Song(genomes, GEN_NUM, x, LENGTH) 
        song_list.append(c)
        song_list[x-1].gen_song()
        x = x + 1

    elif(choice == "7"): #Exports to midi file
      song_choice = (int)(raw_input("Which song would you like to export?\n"))
      file_name = raw_input("Enter filename of midi file you want to create?\n")
      song_list[song_choice-1].export_song(file_name)

    elif(choice == "8"): #exits program
      sys.exit("Program exited")

main()
