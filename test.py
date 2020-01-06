import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np
# import matplotlib.pyplot as plt
# import pickle
from torch.utils.data.sampler import SubsetRandomSampler

from model1 import LSTM

#%%

model = LSTM()
model.load_state_dict(torch.load("checkpoint_1_64.pt", map_location=torch.device("cpu")))
model.eval()

#%%

base = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
words = base + [k + "m" for k in base]  # all possible chords
char_to_int = dict((c, i) for i, c in enumerate(words))

def char_to_vector(chord):
    v = [0 for _ in range(24)]
    i = char_to_int[chord]
    v[i] = 1
    return v

#%%

def printpred(list):
    sequence = [[char_to_vector(chord) for chord in list]]
    prediction = model(torch.as_tensor(sequence, dtype=torch.float)).exp().view(-1)
    dict = {}
    for i in np.asarray(prediction.tolist()).argsort()[::-1]:
        dict[words[i]] = prediction.tolist()[i]
        ##print((words[i] + ":").ljust(5) + str(prediction.tolist()[i]))
    return dict

printpred("A B".split())
