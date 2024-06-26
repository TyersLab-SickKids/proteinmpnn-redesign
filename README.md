# ProteinMPNN Redesign
Implementation of the ProteinMPNN redesign approach by [Sumida et al.](https://pubs.acs.org/doi/10.1021/jacs.3c10941) on the SickKids HPC cluster.

Steps:
1. Fix active site residues
2. Fix evolutionarily conserved residues
3. Redesign using ProteinMPNN
4. Validate using AlphaFold2

# TEV Protease
Control enzyme, from [Sumida et al.](https://pubs.acs.org/doi/10.1021/jacs.3c10941).

### ProteinMPNN

Fix active site and evolutionarily highly conserved residues. **Cysteine** was excluded from possible amino acids that could be designed. Three temperatures (**0.1**, **0.2**, **0.3**) were sampled.

* 8x3 = **24** sequences generated with **only active site** residues fixed
* 8x3 = **24** sequences generated with the active site and **30%** most highly conserved positions fixed
* 16x3 = **48** sequences generated with the active site and **50%** most highly conserved positions fixed
* 16x3 = **48** sequences generated with the active site and **70%** most highly conserved positions fixed

**Note:** The ProteinMPNN output file follows the name of the input PDB. All 1lvm PDBs below are identical, just copied and renamed to reflect the fixed positions of each run. Thus, the input PDB name MUST be unique.
```
sbatch scripts/proteinmpnn.sh <INPUT_PDB> <CHAINS_TO_DESIGN> <FIXED_POSITIONS_JSONL> <NUM_SEQS_PER_TARGET> <OUTPUT_DIR>

sbatch scripts/proteinmpnn.sh inputs/1lvm_active_only.pdb A inputs/active_only.jsonl 8 outputs/TEVd/
sbatch scripts/proteinmpnn.sh inputs/1lvm_top30.pdb A inputs/top30.jsonl 8 outputs/TEVd/
sbatch scripts/proteinmpnn.sh inputs/1lvm_top50.pdb A inputs/top50.jsonl 16 outputs/TEVd/
sbatch scripts/proteinmpnn.sh inputs/1lvm_top70.pdb A inputs/top70.jsonl 16 outputs/TEVd/
```

### Parse FASTA

ProteinMPNN outputs all sequences into a single FASTA file, but AlphaFold2 requires each sequence to be in a separate file with a unique basename. To parse a FASTA file into individual files for each sequence:

```
bash scripts/parse_fasta.sh <INPUT_FASTA> <OUTPUT_DIR>
```

Output FASTAs will be named according to input FASTA name, temperature, and sample number. One will be the original sequence.
