import argparse
from Bio.PDB import PDBParser, NeighborSearch, Selection

def filter_backbone_atoms(substrate_atoms):
    backbone_atoms = []

    for atom in substrate_atoms:
        if atom.get_id() in ['N', 'CA', 'C']:
            backbone_atoms.append(atom)

    return backbone_atoms
def get_residues_within_distance(structure, target_atoms):
    ns = NeighborSearch(target_atoms)
    close_residues = set()

    for residue in structure.get_residues():
        for atom in residue.get_atoms():
            if atom.id in ['N', 'CA', 'C']:
                neighbors = ns.search(atom.coord, 7, 'R')  # 'R' for residues
                if neighbors:
                    close_residues.add(residue)
            else:
                neighbors = ns.search(atom.coord, 6, 'R')  # 'R' for residues
                if neighbors:
                    close_residues.add(residue)
    return close_residues

def select_active_site_residues(protein_pdb, substrate_pdb):
    parser = PDBParser(QUIET=True)

    # Parse the structures
    protein_structure = parser.get_structure('protein', protein_pdb)
    substrate_structure = parser.get_structure('substrate', substrate_pdb)

    # Select atoms from the substrate
    substrate_atoms = Selection.unfold_entities(substrate_structure, 'A')

    # Get residues within the specified distances from protein to substrate
    active_site_residues = get_residues_within_distance(protein_structure, substrate_atoms)

    return active_site_residues

def print_residues(residues):
    for residue in residues:
        print(residue.id[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select active site residues from protein PDB and substrate PDB.')
    parser.add_argument('protein_pdb', type=str, help='Path to the protein PDB file')
    parser.add_argument('substrate_pdb', type=str, help='Path to the substrate PDB file')

    args = parser.parse_args()

    active_site_residues = select_active_site_residues(args.protein_pdb, args.substrate_pdb)
    print_residues(active_site_residues)