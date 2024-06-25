#!/bin/bash

set -e

repo_dir=/hpf/tools/alma8/ProteinMPNN/v1.0.1/

echo Loading module...

module load ProteinMPNN/v1.0.1

name="1lvm_top70"
input_pdb=~/proteinmpnn-redesign/inputs/1lvm.pdb
chains_to_design="A"
fixed_positions=~/proteinmpnn-redesign/inputs/top70.jsonl
output_dir=~/proteinmpnn-redesign/outputs/1lvm/

echo Running script...

python $repo_dir/protein_mpnn_run.py \
	--pdb_path $input_pdb \
	--pdb_path_chains $chains_to_design \
	--fixed_positions_jsonl $fixed_positions \
	--out_folder $output_dir \
	--num_seq_per_target 2 \
	--sampling_temp "0.1 0.2 0.3" \
	--omit_AAs "XC"

output_name=$(basename -- "$input_pdb")
output_name="${output_name%.*}"

# rename output fasta
mv $output_dir/seqs/${output_name}.fa $output_dir/seqs/${name}.fa

echo Done.
