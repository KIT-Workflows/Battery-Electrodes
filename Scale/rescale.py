
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

if __name__ == '__main__':

    with open('bat_input.json') as f:
        data = json.load(f)

    ion_var = data["ion"]
    material_id = data["material-id"]


    structure_charged = read_vasp("POSCAR.charged")
    structure = io.read("POSCAR")

    rescale_structure = get_scaled_supercell(structure,structure_charged)
    del rescale_structure[[atom.index for atom in rescale_structure if atom.symbol == ion_var]]
    write_vasp('POSCAR', rescale_structure, direct=True, vasp5=True)

    

#structure_1 = get_scaled_supercell(structure, structure_charged)
