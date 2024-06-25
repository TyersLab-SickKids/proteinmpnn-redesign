#!/bin/bash

### Helper script to prepare ProteinMPNN output for AlphaFold2.
### Splits one FASTA file into individual FASTA files for each sequence.

### REQUIRED ARGUMENTS
# $1. input .fasta
# $2. output dir

input_fasta=~/proteinmpnn-redesign/outputs/1lvm/seqs/1lvm_top70.fa
output_dir=~/proteinmpnn-redesign/outputs/1lvm/

name=$(basename -- "$input_fasta")
name="${name%.*}"

mkdir -p $output_dir/mpnn/

echo Parsing $name FASTA...

first=true # original sequence

while IFS= read -r line; do
    #  check if line starts with '>' (indicates new sequence)
    if [[ $line == ">"* ]]; then
        
        # first sequence is the original
	if [ "$first" = true ]; then
	    output_fasta="$output_dir/mpnn/${name}-original.fasta"
	    echo "$line" > $output_fasta
	    first=false
	    continue
	fi

        # get temperature and sample number from the sequence identifier
        temp=$(echo "$line" | awk -F '[=,]' '{print $2}')
        sample_num=$(echo "$line" | awk -F '[=,]' '{print $4}')
        
        output_fasta="$output_dir/mpnn/${name}-T${temp}-${sample_num}.fasta"

        # Create a new fasta file with the sample number as the name
        echo "$line" > $output_fasta

    else
        # append the sequence to the corresponding fasta file
        echo "$line" >> $output_fasta
        echo Output to $output_fasta
    fi
done < $input_fasta

echo Done.


