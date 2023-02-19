import os
import chimera
from chimera import runCommand as rc # use 'rc' as shorthand for runCommand
from chimera import replyobj # for emitting status messages
import Midas
import numpy as np
import matplotlib.pyplot as plt

# change to folder with data files
os.chdir("/Users/phong/Desktop/Lynch Lab/Chimera Script")

# gather the names of .pdb files in the folder
ligands_dir = "./ligands"
file_names = [fn for fn in os.listdir(ligands_dir) if fn.endswith(".sdf")]
receptors_dir = "./receptors"
receptor_names = [fn for fn in os.listdir(receptors_dir) if fn.endswith(".pdb")]
vina_location = "'C:/Program Files (x86)/The Scripps Research Institute/Vina/vina.exe'"
output_location = "'C:/Users/phong/Desktop/Lynch Lab/Chimera Script/output/test"
xyz_cords = "-29.1,27.7,17.7"
xyz_size = "34.1,23.7,25"
number_test = 2
steps = 4000
# loop through the files, opening, processing, and closing each in turn
for fn in file_names:
	replyobj.status("Processing " + fn) # show what file we're working on
	rc("open " + ligands_dir+"/" + fn)
	rc("addh")
	rc("minimize nogui 'true' nsteps "+str(steps))
	rc("open " + receptors_dir+"/"+receptor_names[0])
	rc("vina docking receptor #1 ligand #0 wait 'true' backend local location " \
	+ vina_location +" search_center "+xyz_cords+" search_size "+xyz_size \
	+ " output "+output_location+str(number_test)+".txt'")
	rc("focus")
	rc("save test"+str(fn)+"_"+str(receptor_names[0]))
	rc("close session")
	number_test+=1
# uncommenting the line below will cause Chimera to exit when the script is done
#rc("stop now")