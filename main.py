import os
import chimera
from chimera import runCommand as rc
from chimera import replyobj
from functions import *
from chimera import openModels, Molecule

os.chdir("/Users/phong/Desktop/Lynch Lab/Chimera Script")

ligands_dir = "./ligands"
file_names = [fn for fn in os.listdir(ligands_dir) if fn.endswith(".sdf")]
receptors_dir = "./receptors"
receptor_names = [fn for fn in os.listdir(receptors_dir) if fn.endswith(".pdb")]
vina_location = "'C:/Program Files (x86)/The Scripps Research Institute/Vina/vina.exe'"
output_location = "'C:/Users/phong/Desktop/Lynch Lab/Chimera Script/output/test"
xyz_cords = "-29.1,27.7,17.7"
xyz_size = "22,20,20"
steps = 4000

def get_atom(model_number, sub_model_number, residue_number, atom_names):
    model_number = int(model_number)
    sub_model_number = int(sub_model_number)
    models = chimera.openModels.list(modelTypes=[Molecule])
    model = next((m for m in models if m.id == model_number and m.subid == sub_model_number), None)
    if model is None:
        raise ValueError("Model with number {model_number}.{sub_model_number} not found")

    residue = None
    for res in model.residues:
        if res.id.position == residue_number:
            residue = res
            break

    if residue is None:
        raise ValueError("Residue {residue_number} not found in model {model_number}.{sub_model_number}")

    for atom_name in atom_names:
        atom = residue.findAtom(atom_name)
        if atom is not None:
            break

    if atom is None:
        raise ValueError("None of the atoms {atom_names} found in residue {residue_number} of model {model_number}.{sub_model_number}")

    return atom, atom_name


for fn in file_names:
    replyobj.status("Processing " + fn)
    name = os.path.splitext(fn)[0]
    open_ligand_and_add_hydrogens(ligands_dir, fn)
    minimize(steps)
    open_receptor(receptors_dir, receptor_names[0])
    perform_docking(vina_location, xyz_cords, xyz_size, output_location, name)


    rc("color green #2.1")
    # rc("open " + receptors_dir + '/mev kinase with mva.pdb')
    # rc("focus #1")

    receptor, receptor_atom_name = get_atom("1", "0", 96, "CA")  # Change the 3rd argument for residue number of receptor atom
    ligand, ligand_atom_name = get_atom("2", "1", 1, ["C1", "C2", "C3"])    # Ligand atom


    # Measure distance 
    point1 = receptor.xformCoord()
    point2 = ligand.xformCoord()
    distance = chimera.distance(point1, point2)

    # Save image
    open_receptor(receptors_dir, receptor_names[1])
    rc("focus #3")
    rc("turn x 10"); rc("turn y 90"); rc("turn z 90"); rc("turn y 90")
    rc("scale 0.35")  

    # Check if distance is greater than 10 Angstroms
    if distance > 10:
        # Show distance measurement
        rc("distance #1:100@CA #2.1@"+str(ligand_atom_name))
        rc("copy file " + "RERUN" + os.path.splitext(fn)[0] + "_" + os.path.splitext(receptor_names[0])[0] + ".png")

    else:
        rc("distance #1:100@CA #2.1@"+str(ligand_atom_name))
        rc("copy file " + "test"+os.path.splitext(fn)[0]+".png")
        rc("save " + os.path.splitext(fn)[0] + "_" + os.path.splitext(receptor_names[0])[0])
    # Close all models
    rc("close session")

