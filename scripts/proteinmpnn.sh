#!/bin/bash

set -e

repo_dir=/hpf/tools/alma8/ProteinMPNN/v1.0.1/

echo Loading module...
module load ProteinMPNN/v1.0.1

name="top70"
input_pdb=~/protein-redesign/inputs/1lvm.pdb
chains_to_design="A"
fixed_positions=~/protein-redesign/inputs/top70.jsonl
output_dir=~/protein-redesign/outputs/

echo Running script...

python $repo_dir/protein_mpnn_run.py \
	--pdb_path $input_pdb \
	--pdb_path_chains $chains_to_design \
	--fixed_positions_jsonl $fixed_positions \
	--out_folder $output_dir/$name/ \
	--num_seq_per_target 16 \
	--sampling_temp "0.1 0.2 0.3" \
	--omit_AAs "XC"

