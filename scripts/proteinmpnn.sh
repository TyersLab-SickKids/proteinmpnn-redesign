#!/bin/bash

### Script to run ProteinMPNN.

set -e

repo_dir=/hpf/tools/alma8/ProteinMPNN/v1.0.1/

echo Loading module...

module load ProteinMPNN/v1.0.1

### REQUIRED PARAMETERS
# 1: input pdb (MUST have a unique name, ProteinMPNN uses this as its output file name)
# 2: chains to design (e.g. "A")
# 3: fixed positions .jsonl
# 4: num sequences to design per temperature per target
# 5: output dir

input_pdb=$1
chains_to_design=$2
fixed_positions=$3
seq_per_target=$4
output_dir=$5

echo INPUT PDB $input_pdb
echo CHAINS TO DESIGN $chains_to_design
echo FIXED POSITIONS $fixed_positions
echo SEQ PER TARGET $seq_per_target
echo OUTPUT DIR $output_dir

echo Running script...

python $repo_dir/protein_mpnn_run.py \
	--pdb_path $input_pdb \
	--pdb_path_chains $chains_to_design \
	--fixed_positions_jsonl $fixed_positions \
	--out_folder $output_dir \
	--num_seq_per_target $seq_per_target \
	--sampling_temp "0.1 0.2 0.3" \
	--omit_AAs "XC"

echo Done.
