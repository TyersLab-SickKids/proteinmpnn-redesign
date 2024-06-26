"""

Get the most conserved residues from the MSA.
Outputs the residues in order from most to least conserved.

argv[1]: msa fasta
argv[3]: output_dir
"""

import os
import sys
import pandas as pd
from pathlib import Path

input_msa = sys.argv[1]
output_dir = sys.argv[2]

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
    sequences = parse_msa(input_msa)
    df = pd.DataFrame(sequences)

    frequencies = get_frequency_counts(df)

    freq_df = pd.DataFrame(frequencies)
    freq_df.index += 1  # start at residue 1
    freq_df.sort_values(by=freq_df.columns[0], ascending=False, inplace=True)

    filename = Path(input_msa).stem
    freq_df.to_csv(output_dir+'/'+filename+'_conserved_resi.csv', index=True, header=False)

if __name__ == "__main__":
    main()
