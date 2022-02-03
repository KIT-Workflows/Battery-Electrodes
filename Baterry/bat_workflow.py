
import json
from symtable import Symbol

from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp import Poscar
from pymatgen.core import Molecule, Structure


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

    with MPRester(api_key="sNS1eGDdAKTxwOpQ") as mpr:

        # Structure for material id
        struct = mpr.get_structure_by_material_id(material_id) # LiNO3: mp-8180, chevrel: mp-677217, (Spinel) MgTi2O4: mp-27872
        poscar = Poscar(struct)
        poscar.write_file('POSCAR')

    # ASE 

    structure = io.read("POSCAR")

    structure_charged = io.read("POSCAR")

    del structure_charged[[atom.index for atom in structure_charged if atom.symbol == ion_var]]

    write_vasp('POSCAR.charged', structure_charged, direct=True, vasp5=True, label=material_id)

    #structure_1 = get_scaled_supercell(structure, structure_charged)
