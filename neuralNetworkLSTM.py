#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  R E S E A U   D E    N E U R O N E S    L S T M                                    #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                Imported libraries                                                   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow.keras as keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer
from keras.optimizers import RMSprop

sys.path.append("/Users/Rick/Desktop/BE/DataManagement")
import dataManagement as dm

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                   Data preparation                                                  #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

repertoryPath = '/Users/Rick/Desktop/BE/ClassifiedDataTest'

# Get data from csv files
inputData = dm.getData(repertoryPath)
trainingData = inputData[0]
testingData = inputData[1]

# Delete date of the DataFrame
trainingData = trainingData.drop("date", axis=1)
testingData = testingData.drop("date", axis=1)

# Normalizing training data
trainingData = dm.normalize(trainingData)

# Normalizing testing data
testingData = dm.normalize(testingData)

# Splitting inputData and outputData
data = dm.splitData(repertoryPath, trainingData, testingData)
inputTrainingData = np.array(data[0][0])
outputTrainingData = np.array(data[0][1])
inputTestingData = np.array(data[1][0])
outputTestingData = np.array(data[1][1])

# Reshape input data
inputTestingData = dm.reshapeData(inputTestingData)
outputTestingData = dm.reshapeData(outputTestingData)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                   Model Creation                                                    #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Initiate model
model = Sequential()
 
# Add an input layer
model.add(InputLayer(input_shape=(int(dm.setSize(repertoryPath)*0.8), 1)))

# Add a LSTM layer
model.add(LSTM(128))
 
# Add an output layer
model.add(Dense(dm.setSize(repertoryPath) - int(dm.setSize(repertoryPath)*0.8)))

# Model summarize
model.summary()

# Compile the model
opt = RMSprop(lr=0.0001)
model.compile(loss='binary_crossentropy', optimizer= opt)

# Training & Prediction
history = model.fit(x=inputTrainingData, y=outputTrainingData, steps_per_epoch=20, epochs=200, validation_data = 
                    (inputTestingData, outputTestingData) , validation_steps=5)

# Plot prediction ?

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                        E N D                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#