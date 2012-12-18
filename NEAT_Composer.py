import MultiNEAT as NEAT
from mingus.midi import fluidsynth
from mingus.containers.Track import Track
from mingus.containers.Bar import Bar
from mingus.containers.Note import Note
from mingus.core import *
import random
import sys

leader_count = 0
notes = [] #Holds all possible notes
song_pop=[] #Contains the song rep of every network in current gen
leader_list = [] #Contains a list of current leaders (see get_leader method)

fluidsynth.init("FluidR3_GM.sf2", "alsa") #for windows systems, go ahead and remove the comma and "alsa"

#Various parameters for NEAT...will probably change a lot of this
params = NEAT.Parameters()
params.PopulationSize = 10

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

#class Song:   Not Sure if necessary, just make a list for the actual songs
#  song = Track()
#  fitness = 0
#  length = 0
#  def __init__(self, song, fitness):
#    self.song = song
#    self.fitness = fitness

def gen_Song(genome): #Generates song based on output of a neural network
  global song_pop
  net = NEAT.NeuralNetwork()
  genome.BuildPhenotype(net)
  time = 0.0 #input which tracks total time through song from. Song is 8 notes in this test 
  beat = 0.25 #input which tracks beat in measure [.25-1]
  track = Track()
  
  while(time <= 0.999999):
    net.Input([time, beat])
    net.Activate()
    output = net.Output()[0]*88
    track + notes[int(output)]
    beat = (beat+.25)%1
    time = time + (1.0/16.0)
  song_pop.append(track)
  
  
    
    
def evaluate(song): #Checks ratio of notes in a song are in a certain scale to total
  sum = 0
  for x in range(0,16):
    note = song[x/4][x%4][2][0]
    if(note > 24) and (note < 35):
      sum = sum+1
  return sum/16.0


def play_song(pop_member): #Plays a selected song
  fluidsynth.play_Track(pop_member, 1, 150) #For increased/decreased tempo, change the 150
  return

def print_pop(): #Prints the population of songs
  x = 1
  for song in song_pop:
    print x
    for y in range(0,4): 
      for num in range(0,4): print(song[y][num][2][0]),

    print
    x = x+1
    
def get_leader(g_list): #Gets leader of an entire generation and returns a list
                        #with the network num, the network, and it's fitness.
  global leader_count
  c_fit = 0
  count = 0
  leader_c = 0
  leader_genome = g_list[0]
  leader_fit = 0
  for genomes in g_list:
    c_fit = genomes.GetFitness()
    if(leader_fit < c_fit):
      leader_fit = c_fit
      leader_genome = genomes
      leader_c = count
    count = count +1
  leader_count = leader_count +1
  return [leader_c, leader_genome, leader_fit]
      


def main():
  global notes
  global song_pop
  genome = NEAT.Genome(0,2,0,7,False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, params)
  pop = NEAT.Population(genome, params, True, 1.0) 
  numb = 9
  while(numb<97):
    c = Note()
    notes.append(c.from_int(numb))
    numb = numb+1
  programrun = 1
  genome_list = NEAT.GetGenomeList(pop)
  for genomes in genome_list:
    gen_Song(genomes)
  while(programrun == 1):
    choice = raw_input("Choose one of the following\n1) Print population\n2) Eval population using fitness func\n3) Manually set fitness\n4) Print pop Fitness\n5) Play pop member\n6) Pop epoch\n7) Print leaders\n8) Quit\n")
    if(choice == "1"): #Print population
      print_pop()

    elif(choice == "2"): #Evaluate using fitness
      choice = raw_input("How many generations would you like to run?\n")
      for y in range(0, int(choice)-1):
        x = 0
        for genomes in genome_list:
          genomes.SetFitness(evaluate(song_pop[x]))
          x=x+1
        leader = get_leader(genome_list)
        leader_list.append(leader)
        pop.Epoch()
        song_pop = []
        genome_list = NEAT.GetGenomeList(pop)
        for genomes in genome_list:
          gen_Song(genomes)
      x = 0
      for genomes in genome_list:
        genomes.SetFitness(evaluate(song_pop[x]))
        x = x+1
      leader_list.append(get_leader(genome_list))
    
    elif(choice == "3"): #Selects a member of the population and sets its fitness manually
      song_select = raw_input("What member's fitness do you want to set?\n")
      new_fit = raw_input("Enter desired fitness\n")
      old_fit = genome_list[int(song_select) - 1].GetFitness()
      genome_list[int(song_select)-1].SetFitness(float(new_fit))
      print "Member", song_select,"fitness changed from", old_fit, "to", new_fit,"\n"
      
    elif(choice == "4"): #print fitness of pop
      x = 1
      for genomes in genome_list:
        print "Song", x, "has fitness of", genomes.GetFitness(), "\n"
        x =  x+1

    elif(choice == "5"): #Play pop member
      choice = raw_input("What member would you like to play?\n")
      play_song(song_pop[int(choice)-1])

    elif(choice == "6"): #Pop epoch
      pop.Epoch()
      song_pop = []
      genome_list = NEAT.GetGenomeList(pop)
      for genomes in genome_list:
        gen_Song(genomes)
     
    elif(choice == "7"): #Prints the leaders of each generation
      x = 1
      for leader in leader_list:
        print "Member", leader[0]+1, "in gen", x, "has fitness of", leader[2]
        x = x + 1
        

    elif(choice == "8"): #Exit program
      sys.exit("Program exited")

    else:
      print "Not a valid choice, choose again.\n"

main()
