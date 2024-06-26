"""

Get the most conserved residues from the MSA.
Outputs the residues in order from most to least conserved.

argv[1]: input msa fasta
argv[3]: output_dir

"""

import os
import sys
import pandas as pd
from pathlib import Path

name = sys.argv[1]
input_msa = sys.argv[2]
output_dir = sys.argv[3]

def parse_msa(msa_file):
    sequences = []
    with open(msa_file, 'r') as f:
        sequence = ''
        for line in f:
            if line.startswith('>'):
                if sequence:
                    sequences.append(list(sequence.strip()))
                    sequence = ''

            else:
                sequence += line.strip()
        if sequence: # last sequence
            sequences.append(list(sequence.strip()))
    return sequences

def get_frequency_counts(df):
    """
    Get the frequency of the most frequent residue in each column.
    """
    frequency_counts = []
    for col in df.columns:
        col_data = df[col]
        col_data = col_data[(col_data != '-')]
        if col_data.empty:
            frequency_counts.append(0)
        else:
            frequency_counts.append(col_data.value_counts().iloc[0])
    return frequency_counts

def main():

    print('Parsing MSA')

    sequences = parse_msa(input_msa)
    df = pd.DataFrame(sequences)

    # remove residues that don't exist in the template
    drop_cols = [c for c in df.columns if df[c].iloc[0] == '-']
    print('Drop columns from template', drop_cols)
    df = df.drop(columns=drop_cols)

    print('Num sequences:', len(df))
    print('Num residues per sequence:', len(df.columns))

    frequencies = get_frequency_counts(df)

    freq_df = pd.DataFrame({'residue': range(1, len(frequencies)+1),
                            'frequency': frequencies})
    freq_df.sort_values(by='frequency', ascending=False, inplace=True)

    filename = Path(input_msa).stem
    output_file = output_dir + '/conserved_resi_' + filename + '.txt'
    freq_df.to_csv(output_file, index=False, header=True)
    print('All residues output to', output_file)
    print('Done.')

if __name__ == "__main__":
    main()
