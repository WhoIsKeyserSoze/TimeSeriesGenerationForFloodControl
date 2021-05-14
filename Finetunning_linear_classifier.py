import pandas as pd
import os
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas
from tensorflow import keras
import numpy as np

# ------------------------------------- #
# Parameters
# ------------------------------------- #

# data parameters :
data_path = 'D:\Desktop\Prog\L3\BE\WorkBench\RandomST'
manual_data_test_path = 'D:\Desktop\Prog\L3\BE\WorkBench\\testData'


# rnn parameters :
sequence_len = 24 * 3  # 3 days of measures
save_dir = "D:\Desktop\Prog\L3\BE\WorkBench\Temp_test_save_rnn"


# ------------------------------------- #
# Gather data
# ------------------------------------- #

# put data from file to an array
def loadST(file_name, data_path):
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
        label = [1]
    else:
        label = [0]

    return final_list, [label]

# for all files :
#   read file
#   then gather all height measure
#   then normalize measures
#   then put this list in dataset
# then make trainList and testList


dataset = []
labels = []
n = 0
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        st, label = loadST(file, data_path)
        st = np.array(st)
        st = (st - st.mean()) / st.std()
        dataset.append(st)
        labels.append(label)
        n += 1

dataset = np.array(dataset)
labels = np.array(labels)

p = int(n*0.85)
trainX = dataset[0:p:1]
testX = dataset[p:n:1]

trainY = labels[0:p:1]
testY = labels[p:n:1]

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


# print(model.predict(np.array([x])))

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])


# ------------------------------------- #
# train it
# ------------------------------------- #

history = model.fit(x=trainX, y=trainY, epochs=50,
                    validation_data=(testX, testY))

# ------------------------------------- #
# test it
# ------------------------------------- #


for file in os.listdir(manual_data_test_path):

    testST, label = loadST('2021-03-30_A261020001_L.csv',
                           manual_data_test_path)
    print("File name : " + file + "\nLabel : " + str(label) + "\nPrediction : " + str(model.predict(np.array([testST]))))

    df = pandas.read_csv(data_path + '\\' + file)
    fig, ax = plt.subplots()

    df.plot(kind='line', x='date', y='height', ax=ax)
    fig.tight_layout()
    plt.show()
