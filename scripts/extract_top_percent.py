"""

From the list of most conserved residues and their frequencies,
extract the top X% and output to a .jsonl file for ProteinMPNN residue fixing.

argv[1]: Name of output .jsonl file. MUST match the input PDB it is paired with for ProteinMPNN.
argv[2]: Chain (e.g. "A")
argv[3]: Conserved residues .txt. Assumes in descending frequency order. 
argv[4]: X, for top X%
argv[5]: output_dir

"""

import os
import sys
from pathlib import Path
import pandas as pd
import math
import json

name = sys.argv[1]
chain = sys.argv[2]
input_file = sys.argv[3]
percent = int(sys.argv[4])
output_dir = sys.argv[5]

def main():

    print('Reading input file')

    df = pd.read_csv(input_file)

    # get number of residues in top%
    num_residues = len(df)
    num_in_top_percent = math.floor(num_residues * percent / 100)

    print('Num residues in top percent', num_in_top_percent)

    # if there is a tie at the cutoff, get fewer residues
    if df.iloc[num_in_top_percent-1, 1] == df.iloc[num_in_top_percent, 1]:
        freq_cutoff = df.iloc[num_in_top_percent-1, 1]
        top_df = df[df.iloc[:,1] > freq_cutoff]
    else:
        top_df = df.head(num_in_top_percent)
    print('Num residues after ties', len(top_df))

    residue_list = top_df.iloc[:,0].tolist()
    residue_list.sort()
    print('Residue list', residue_list)

    # create dict
    json_dict = {
        name: {
            chain: residue_list
        }
    }

    print('json dict', json_dict)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file = output_dir + '/' + name + '.jsonl'

    # dump to jsonl
    with open(output_file, 'w') as outfile:
        json.dump(json_dict, outfile)

    print('Output to', output_file)
    print('Done.')

if __name__ == "__main__":
    main()

