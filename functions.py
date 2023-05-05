import os
import chimera
from chimera import runCommand as rc
from chimera import openModels
from chimera import Molecule

def build_molecule_from_smiles(smiles_str):
    rc("open smiles:" + smiles_str)
    rc("addh")
    
def open_ligand_and_add_hydrogens(ligands_dir, file_name):
    rc("open " + ligands_dir + "/" + file_name)
    rc("addh")

def minimize(nsteps):
    rc("minimize nogui 'true' nsteps " + str(nsteps))

def open_receptor(receptors_dir, receptor_name):
    rc("open " + receptors_dir + "/" + receptor_name)

def perform_docking(vina_location, xyz_cords, xyz_size, output_location, name):
    rc("vina docking receptor #1 ligand #0 wait 'true' backend local location "
       + vina_location + " search_center " + xyz_cords + " search_size " + xyz_size
       + " output " + output_location + str(name) + ".txt'")

def select_mev_binding_pocket():
    rc("distance #1:100@CA #2.1@C1")


