#!/bin/bash

# Extract pLDDT scores from AF2 and calculate Calpha RMSD between original structure and AF2 design.

# Required arguments:
# $1: output AF2 directory
# $2: original PDB (to calculate Calpha RMSD)
# $3: output dir

af2_dir=$1
original_pdb=$2
output_file=$3/scores.txt

fmt="%s\t%s\t%s\t%s\n"

echo Output $output_file

printf "$fmt" pLDDT Calpha_RMSD af2_design successful > $output_file

for dir in $af2_dir/*; do
	pkl_file="${dir}/result_model_3_pred_0.pkl"
	af2_pdb="${dir}/unrelaxed_model_3_pred_0.pdb"
	
	if [ -f "$pkl_file" ] && [ -f "$af2_pdb" ]; then
		echo $(basename $dir)
		
		plddt=$(python calculate_plddt.py $pkl_file)
		calpha_rmsd=$(python calculate_rmsd.py "$original_pdb" "$af2_pdb")
	
		pass_plddt=$(echo "$plddt > 85" |bc -l)
		pass_rmsd=$(echo "$calpha_rmsd < 2" |bc -l)

		if [ "$pass_plddt" = "1" ] && [ "$pass_rmsd" = "1" ]; then
			successful=true
	        else
		 	successful=false	
		fi

		printf "$fmt" $plddt $calpha_rmsd $(basename $dir) $successful >> $output_file

	fi
done

echo Done.
