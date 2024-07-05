#!/bin/bash

set -e

repo_dir=/hpf/tools/centos7/alphafold/2.3.2/

input_dir=$1
output_dir=$2

echo Loading module...

module load alphafold/2.3.2

echo Getting input FASTAs..

fasta_paths=""

for filename in $input_dir/*.fasta; do
    fasta_paths+=$(realpath "$filename"),
done

echo $fasta_paths

echo Running script...

alphafold --output_dir=$output_dir/af2/ \
	--fasta_paths=$fasta_paths \
	--data_dir=$repo_dir/data/ \
	--max_template_date=2024-01-01 \
	--uniref90_database_path=$repo_dir/data/uniref90/uniref90.fasta \
	--mgnify_database_path=$repo_dir/data/mgnify/mgy_clusters_2022_05.fa \
	--template_mmcif_dir=$repo_dir/data/pdb_mmcif/mmcif_files \
	--obsolete_pdbs_path=$repo_dir/data/pdb_mmcif/obsolete.dat \
	--use_gpu_relax=true \
	--db_preset=reduced_dbs \
	--small_bfd_database_path=$repo_dir/data/small_bfd/bfd-first_non_consensus_sequences.fasta \
	--pdb70_database_path=$repo_dir/data/pdb70/pdb70

echo Done.
