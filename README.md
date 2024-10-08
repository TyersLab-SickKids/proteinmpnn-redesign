# ProteinMPNN Redesign
Implementation of the ProteinMPNN redesign approach by [Sumida et al.](https://pubs.acs.org/doi/10.1021/jacs.3c10941) on the SickKids HPC cluster.

### Steps:
1. Fix active site residues
2. Fix evolutionarily conserved residues
3. Redesign using ProteinMPNN
4. Validate using AlphaFold2

# Targets of Interest
### TEV Protease
Control enzyme, from [Sumida et al.](https://pubs.acs.org/doi/10.1021/jacs.3c10941)
### PETase
Target of interest, see [Han et al.](https://www.nature.com/articles/s41467-017-02255-z)

# Pipeline
### Active Site Residues
Fix residues containing:
* **Backbone** atoms within **7** angstroms of the substrate, or
* **Sidechain** atoms within **6** angstroms of the substrate
```
python scripts/bindingsite_selection.py <target_pdb> <ligand_pdb> <output_file_name> <chain> <output_dir>
```

**IMPORTANT NOTE:** The target PDB **MUST** start at residue index 1 and not have any discontinuities. This is because when fixing residues in ProteinMPNN, ProteinMPNN considers "residue 1" as the "1st residue" and not "the residue with index 1".

### Evolutionarily Conserved Residues
Determined through Multiple Sequence Alignment (MSA) with four iterative [HHblits](https://toolkit.tuebingen.mpg.de/tools/hhblits) searches against the UniRef30 database. Final result filtered with [HHfilter](https://toolkit.tuebingen.mpg.de/tools/hhfilter). If not specified the paramters in HHBlits were left standard
1. HHBlits template sequence with E = **1e-50** set max target hits to 10000
2. Forward A3M to HHblits with E = **1e-30**
3. Forward A3M to HHblits with E = **1e-10**
4. Forward A3M to HHblits with E = **1e-4**
5. Copy Query MSA (dowload full a3m) to HHfilter (upload the same a3m) with Maximal Sequence Identity = **90%**, Minimal Sequence Identity = **30%**, Minimal Coverage = **50%**
6. Rank the residues by their most frequent amino acid frequencies (download the MSA from HHFilter step)
```
python scripts/get_conserved_residues.py <hhfilter_output_msa_fasta> <output_dir>
```

7. Extract the top percent% most conserved positions and create .jsonl for ProteinMPNN
```
python scripts/extract_top_percent.py <name> <chain> <conserved_resi.txt> <percent> <output_dir> <active_site_jsonl>
```

### ProteinMPNN

Fix active site and evolutionarily highly conserved residues. **Cysteine** was excluded from possible amino acids that could be designed. Three temperatures (**0.1**, **0.2**, **0.3**) were sampled.

* 8 x 3 = **24** sequences generated with **only active site** residues fixed
* 8 x 3 = **24** sequences generated with the active site and **30%** most highly conserved positions fixed
* 16 x 3 = **48** sequences generated with the active site and **50%** most highly conserved positions fixed
* 16 x 3 = **48** sequences generated with the active site and **70%** most highly conserved positions fixed

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

### AlphaFold2

Model 3, 6 recycles. Structural templating and MSA of the parent sequence was used for all designs.

Using regular AlphaFold2 with all five models, 3 recycles, database template search and each respective design their own MSA:
```
sbatch --time=10:00:00 --tmp=64G --mem=64G -G 1 scripts/alphafold.sh <INPUT_DIR> <OUTPUT_DIR>
```
where `<INPUT_DIR>` is the output of the previous Parse FASTA step.

To use a modified verison of alphafold with Model 3, 6 recycles
```
sbatch --time=10:00:00 --tmp=64G --mem=64G -G 1 scripts/alphafold_v2.sh <INPUT_DIR> <OUTPUT_DIR>
```
To calculate and consolidate the scores:
```
# enter compute node
srun --pty bash -l
module load python/3.11.3

bash scripts/filter_scores.sh <AF2_OUTPUT_DIR> <ORIGINAL_PDB> <OUTPUT_DIR>
```
Where `filter_scores.sh` calls `calculate_plddt.py` ~~and `calculate_rmsd.py`~~.

**UPDATE:** We recommend manually calculating the Calpha RMSD in PyMOL. Do not use the RMSD column in the output scores file; it has not been validated. To calculate RMSD in PyMOL:

```
align <af2_predicted_structure> and name CA, <original_pdb> and name CA
```

### Success
A successful sequence is defined as pLDDT > 85.0 and Calpha RMSD < 2.0 Angstrom.
