import pandas as pd
import os
import graph
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

# ------------------------------------- #
# Parameters
# ------------------------------------- #

# data parameters :
data_path = 'D:\Desktop\Prog\L3\BE\WorkBench\RandomST'


# rnn parameters :
sequence_len = 24 * 3  # 3 days of measures
save_dir = "D:\Desktop\Prog\L3\BE\WorkBench\Temp_test_save_rnn"


# ------------------------------------- #
# Gather data
# ------------------------------------- #

# put data from file to an array
def loadST(file_name):
    df = pd.read_csv(data_path + '\\' + file)
    arr = df.to_numpy()
    final_list = []
    i = 0
    # separate measure and date
    for [date, measure] in arr:
        final_list.append([measure])
        i += 1
    # Because some ST are missing measures and we need all ST to be same length
    # i add the last measure over again until it has 71 measures
    lastmeasure = final_list[-1]
    for j in range(i, 72):
        final_list.append(lastmeasure)

    if(file[-5:-4] == 'L'):
        expected_res = [1]
    else:
        expected_res = [0]

    return final_list, [expected_res]

# for all files :
#   read file
#   then gather all height measure
#   then normalize measures
#   then put this list in dataset
# then make trainList and testList


dataset = []
expected_res = []
n = 0
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        st, st_res = loadST(file)
        #st = (st - st.mean()) / st.std()
        dataset.append((st, st_res))
        n += 1

p = int(n*0.85)
trainset = np.array(dataset[0:p:1])
testset = np.array(dataset[p:n:1])

# ------------------------------------- #
# set up RNN
# ------------------------------------- #
# note : we want a RNN that takes a ST and gives a number between 0 and 1


model = keras.models.Sequential()
#input Layer
model.add(keras.layers.InputLayer(input_shape=(72, 1)))
# Add a LSTM layer with 128 internal units.
model.add(keras.layers.LSTM(128))
# Output layer
model.add(keras.layers.Dense(1))

model.summary()


print(model.predict(np.array([trainset[0][0]])))


# ------------------------------------- #
# train it
# ------------------------------------- #


# ------------------------------------- #
# test it
# ------------------------------------- #
