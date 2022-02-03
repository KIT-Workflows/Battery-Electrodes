
import yaml, json

from ase import io
from ase.io.vasp import read_vasp, write_vasp

def get_volume_change(atoms_full, atoms_empty):
    """ Returns the volume change between two structures

    Parameters
    ----------
    atoms_full : ase-atoms object
        Fully discharged phase - all ions in structure
    atoms_empty : ase-atoms object
        Fully charged phase - ion emptied

    Returns
    --------
    v_change : float
        Volume chang in percent

    """
    v_full = atoms_full.get_volume()
    v_empty = atoms_empty.get_volume()
    v_change = ((v_empty - v_full)/v_full) * 100

    return v_change


def get_scaled_supercell(supercell, supercell_empty):
    """ Returns scaled supercell without any defect """
    # when supercell_empty==None no re-scale
    sc_copy = supercell.copy()
    if supercell_empty:
        sc_copy = supercell.copy()
        # atoms = empty supercell
        # supercell = bulk ion filled supercell
        # step 1: ratio in volume change empty/filled supercell
        v_empty = supercell_empty.get_volume()
        v_filled = sc_copy.get_volume()
        r = v_empty/v_filled
        # step 2: rescale supercell and atom positions
        scaled_cell = sc_copy.get_cell() * r**(1/3)
        sc_copy.set_cell(scaled_cell, scale_atoms=True)

    return sc_copy

def round_float_list(float_list, decimal_points):
    float_list = [round(float(item),decimal_points) for item in float_list]
    return float_list

if __name__ == '__main__':

    structure_charged = read_vasp("POSCAR.charged")
    structure = io.read("POSCAR")

    v_change = []
    v_change.append(get_volume_change(structure, structure_charged))


    results_dict = {}
    results_dict["v_change"] = round_float_list(v_change,4) 
    with open("decision_1.yml",'w') as out:
        yaml.dump(results_dict, out,default_flow_style=False)

    

#structure_1 = get_scaled_supercell(structure, structure_charged)
