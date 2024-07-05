'''
Adapted from github.com/sarisabbon/RMSD.

Required arguments:
    [1]: PDB #1
    [2]: PDB #2

Prints the Calpha RMSD between the two structures.
'''

import sys

pdb1 = sys.argv[1]
pdb2 = sys.argv[2]

def calculate_calpha_rmsd(structure_1, structure_2):
    """
    Calculate the RMSD between two protein structures using Biopython
    The Biopython algorithm is poorly designed and only aligns local motifs
    rather than full protein structures/complexes.
    """
    import Bio.PDB
    builder = Bio.PDB.Polypeptide.PPBuilder()
    
    STR1 = builder.build_peptides(Bio.PDB.PDBParser(QUIET=True)\
            .get_structure('Structure 1', structure_1), aa_only=True)
    STR2 = builder.build_peptides(Bio.PDB.PDBParser(QUIET=True)\
            .get_structure('Structure 2', structure_2), aa_only=True)
    fixed  = [atom for poly in STR1 for atom in poly.get_ca_list()]
    moving = [atom for poly in STR2 for atom in poly.get_ca_list()]
	
    lengths = [len(fixed), len(moving)]
    smallest = min(lengths)
	
    sup = Bio.PDB.Superimposer()
    sup.set_atoms(fixed[:smallest], moving[:smallest])
    sup.apply(Bio.PDB.PDBParser(QUIET=True)\
            .get_structure('Structure 2', structure_2)[0].get_atoms())
	
    RMSD = round(sup.rms, 10)
    return RMSD

def main():
    rmsd = calculate_calpha_rmsd(pdb1, pdb2)
    print(rmsd)

if __name__ == "__main__":
    main()
