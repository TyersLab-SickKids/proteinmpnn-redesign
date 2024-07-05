'''
Extract the AF2 scores produced by the model.

Required arguments:
    [1] : result_model_*.pkl file
'''

import sys
import pickle
import numpy as np
from pathlib import Path

pkl_file = sys.argv[1]

with open(pkl_file, 'rb') as f:
    data = pickle.load(f)

scores = data['plddt']
mean_score = np.mean(scores)

print(mean_score)
