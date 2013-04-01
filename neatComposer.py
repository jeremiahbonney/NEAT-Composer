#NEAT Composer text version. This version uses OOP to make it cleaner 
#and hopefully make transfering to a GUI easier. Also puts fitness
#functions and other messy stuff in the fitness_func.py file.

import sys
import MultiNEAT as NEAT
from mingus.midi import fluidsynth  # Commented out until they work on lab machines
from mingus.midi import MidiFileOut
from mingus.containers.Track import Track
from mingus.containers.Bar import Bar
from mingus.containers.Note import Note
from mingus.core import *
import random
import fitness_func  #contains fitness functions and other useful stuff
from Tkinter import *
from Tkinter import Tk
import tkSimpleDialog
import tkFileDialog
import novelty

fluidsynth.init("FluidR3_GM.sf2", "alsa")
LENGTH = 12.0 #Global var for song length, must be a multiple of 4 for now
GEN_NUM = 0
#Song class that keeps all the information about the song in one place, including
#the track itself, it's fitness, what generation it belongs to, it's length, etc
params = NEAT.Parameters()
params.PopulationSize = 12

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
  novelty_params = []
  novelty_score = 0
  

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
    str_song = str(self.song_id) + " "
    for x in range(0,(int)(self.length/4)):
      for num in range(0,4): str_song = str_song + str(self.song[x][num][2][0])
    
#    print
    return str_song

  def play_song(self):  #Plays the song at 150 BPM using fluidsynth(make BPM a var later?)
    fluidsynth.play_Track(self.song, 1, 150)
    return

  def export_song(self, filename):
    MidiFileOut.write_Track(filename, self.song, self.bpm, 0)
    #pass
    
#End of Song Class


def evaluate(a_song, fitness_func, genome, *args):      #Takes a song and fitness function, then evaluates
  a_song.fitness = fitness_func(a_song, *args)
  genome.SetFitness(a_song.fitness); 
	 #the song via that fitness function. Also sets the
  return a_song.fitness 				         #song_fitness attribute


def advance_gen(genome_list):  #Advances population to next generation
  global GEN_NUM
  song_list2 = []
  x = 1
  GEN_NUM = GEN_NUM+1
  for genomes in genome_list:
    c = Song(genomes, GEN_NUM, x, LENGTH)
    song_list2.append(c)
    song_list2[x-1].gen_song()
    x = x+1
  return song_list2

def redraw_listbox():
  listbox.delete(0, END);
  for song in song_list:
    listbox.insert(END, "Song: %d.%d" %(GEN_NUM, song.song_id) + "    Fitness:" + str( song.fitness) + "    Novelty:" + str(song.novelty_score))


def song_clicked(i):
  index = int(listbox.curselection()[0])
  print(song_list[index].print_song())
  song_list[index].play_song()

def print_all():
  for song in song_list:
    print song.print_song() + "\n" 
  print "\n" 

def print_song_prop():
  pass

def in_key_choice():
  global choice
  choice = tkSimpleDialog.askstring("Key Choice", "Enter key you with to restrict to")
  print "In key choice is", choice

def evaluate_pop():
  args = (choice)
  in_key_offset = in_key_slider.get()
  diatonic_offset = diatonic_slider.get()
  in_key_fitness = 0
  diatonic_fitness = 0
  y = 0
  for genomes in genome_list:
    in_key_fitness = evaluate(song_list[y], fitness_func.functions["in_key"], genomes, *args)
    diatonic_fitness = evaluate(song_list[y], fitness_func.functions["diatonic"], genomes, *args)
    song_list[y].fitness = (in_key_fitness*in_key_offset + diatonic_fitness*diatonic_offset)/2.0
    y = y+1
  redraw_listbox()

def evolve_pop():
  global population
  global song_list
  global genome_list
  population.Epoch()
  genome_list = NEAT.GetGenomeList(population)
  song_list = advance_gen(genome_list)
  redraw_listbox()

def export():
  filename = tkFileDialog.asksaveasfilename(parent = root)
  song = listbox.index(ACTIVE)
  print filename, song
  song_list[song].export_song(filename)
  
def novelty_func():
  novelty.set_novelty_params(song_list)
  novelty.novelty_search(song_list)
  redraw_listbox()
    
  


choice = "C"


population = NEAT.Population(genome, params, True, 1.0)
genome_list = NEAT.GetGenomeList(population)
song_list = advance_gen(genome_list)



root = Tk()
root.wm_title("NEAT Composer")

frame = Frame(root)

frame.grid(row=0, column=0)

framenovelty = Frame(root)
framenovelty.grid(row=0, column=1)

framelistbox = Frame(root)
framelistbox.grid(row = 0, column = 2)



nov1 = IntVar()
nov1.set(0)
nov2 = IntVar()
nov2.set(0)
nov3 = IntVar()
nov3.set(0)

evaluateButton = Button(frame, text = "Evaluate population", command = evaluate_pop)
evaluateButton.grid(row = 4, column = 0)

noveltyButton = Button(framenovelty, text = "Use Novelty", command = novelty_func)
noveltyButton.grid(row=4, column = 0)

evolveButton = Button(frame, text = "Evolve population", command = evolve_pop)
evolveButton.grid(row = 5, column = 0)

menu = Menu(root)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu = filemenu)
filemenu.add_command(label = "Export Song", command = export)

viewmenu = Menu(menu)
menu.add_cascade(label = "View", menu = viewmenu)
viewmenu.add_command(label = "Print all", command = print_all)

root.config(menu = menu)

yscroll = Scrollbar(framelistbox, relief = 'raised')
yscroll.grid(row=0, column=1)


listbox = Listbox(framelistbox, yscrollcommand = yscroll.set, width = 40, height = 8)
for song in song_list:
  listbox.insert(END, "Song: %d.%d" %(GEN_NUM, song.song_id) + "    Fitness:" + str( song.fitness) + "    Novelty:" + str(song.novelty_score))

listbox.grid(row = 0, column = 0)
yscroll.config(command = listbox.yview)
listbox.bind('<<ListboxSelect>>', song_clicked)

fitnesslabel = Label(frame, text = "Fitness Functions")
fitnesslabel.grid(row = 0, column = 0)
noveltylabel = Label(framenovelty, text= "Novelty Parameters")
noveltylabel.grid(row=0, column=0)

song_slope_button = Checkbutton(framenovelty, text = "Song Slope", variable = nov1, offvalue=0, onvalue=1)
song_slope_button.grid(row = 1, column = 0)

song_var_button = Checkbutton(framenovelty, text = "Song Variance", variable = nov2, offvalue = 0, onvalue=1)
song_var_button.grid(row = 2, column = 0)
song_range_button = Checkbutton(framenovelty, text = "Song Range", variable = nov3, offvalue = 0, onvalue = 1)
song_range_button.grid(row=3, column = 0)


in_key_button = Button(frame, text = "Set Key", command = in_key_choice)
in_key_button.grid(row=1, column=0)
in_key_slider = Scale(frame, from_=-100, to=100, orient=HORIZONTAL, label="InKey")
in_key_slider.grid(row=2, column=0)
diatonic_slider = Scale(frame, from_=-100, to=100, orient=HORIZONTAL, label="Diatonic")
diatonic_slider.grid(row=3, column=0)

root.mainloop()
