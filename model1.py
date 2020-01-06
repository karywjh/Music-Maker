# %%

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# import numpy as np
# import matplotlib.pyplot as plt
# import pickle

# from music_preprocessing import MusicData
from torch.utils.data.sampler import SubsetRandomSampler

# %%


class LSTM(nn.Module): # define our LSTM network
    def __init__(self):
        super(LSTM, self).__init__()
        self.lstm = nn.LSTM(24, 64, 2, dropout=0.2)  # input size 24 (for one hot), hidden state size 64, total layers 2
        self.linear = nn.Linear(64, 24)  # linear layer with input size 64 and output size 24

    def forward(self, sequence):
        lstm_out, _ = self.lstm(sequence.transpose(0, 1))  # lstm_out dimensions: [output_sequence, batch_size, 24]
        logits = self.linear(lstm_out[-1, :, :].view(-1, 64))  # process the last output of the LSTM block
        prediction = F.log_softmax(logits, dim=1)  # softmax layer to convert to probabilities

        return prediction
