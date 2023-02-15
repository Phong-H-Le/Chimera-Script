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
steps = 1000
# loop through the files, opening, processing, and closing each in turn
for fn in file_names:
	replyobj.status("Processing " + fn) # show what file we're working on
	rc("open " + ligands_dir+"/" + fn)
	# rc("align ligand ~ligand") # put ligand in front of remainder of molecule
	rc("select")
	rc("focus #0") # center/zoom ligand
	# rc("surf") # surface receptor
	# rc("preset apply publication 1") # make everything look nice
	# rc("surftransp 15") # make the surface a little bit see-through
	# save image to a file that ends in .png rather than .pdb
	# png_name = fn[:-3] + "png"
	# rc("copy file " + png_name + " supersample 3")
	rc("addh")
	rc("minimize nogui 'true' nsteps "+str(steps))
	rc("open " + receptors_dir+"/"+receptor_names[0])
	rc("vina docking receptor #1 ligand #0 wait 'true' backend local location " \
	+ vina_location +" search_center "+xyz_cords+" search_size "+xyz_size \
	+ " output "+output_location+str(number_test)+".txt'")
	number_test+=1
	rc("close all")

# uncommenting the line below will cause Chimera to exit when the script is done
#rc("stop now")