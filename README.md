NEAT-Composer
=============
NEAT-Composer is a interactive evolutionary tool designed to allow the user to compose songs using a variety of methods 
including NEAT and Novelty Search. 
As is probably evident, this is far from finished, but I'll give a breakdown of what it does so far.

First off, to get the code to run you need several things. MultiNEAT, fluidsynth, and Mingus. See their respective
pages to figure out how to get and configure these packages.

As to what actually works, I have a basic GUI iterface which allows evolution using either fitness functions, novelty search, 
or manually setting the fitness. The fitness functions, as well as some other useful stuff, is located in the file
fitness_func.py and the novelty search stuff is in novelty.py . I also have playing the songs and exporting them as MIDI files working (I think the MIDI exporting works
anyway). Take a look at the main file neatComposer.py for more information.


