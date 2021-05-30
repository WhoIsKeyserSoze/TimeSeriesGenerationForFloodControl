import os

from tensorflow import keras

import TimeSeriesPredictor as tsp

# This programme train a neural network and save it
# It will try to download, store and prepare data from hubeau api
# Data download will probably take the most time since you'll need a lot of it
# to download data there is a line (27) to uncomment


#---------------#
# Prepare data  #
#---------------# 

# change it to the location where you want to save the data required to train the network

data_path = ".\\data"
network_storage = "BILSTM"


trainning_proportion = 0.85
nb_rawSeries_to_download = 100
rawSeries_len = 29*24 #29 days and 24 hours of measurments

# First donwload tons of measures from hubeau api's
# if already done, comment next line of code
#LSTMdata.random_data_geter(nb_rawSeries_to_download, data_path, period=int(rawSeries_len/24))

# then load them into a nice list

rawData = tsp.BILSTM.BILSTMdata.load_data(data_path, rawSeries_len)
rawData = tsp.BILSTM.BILSTMdata.normalize_dataset(rawData)

# making many nb_day long time series from the raw data
dataset = tsp.BILSTM.BILSTMdata.timeSeriesGenerator(rawData, rawSeries_len, 24)

p = int(trainning_proportion * len(dataset[0]))
trainData_x = dataset[0][:p]
trainData_y = dataset[1][:p]

testData_x = dataset[0][p:]
testData_y = dataset[1][p:]

#---------------#
# prepare model #
#---------------#

model = keras.models.Sequential()
# Input layer
model.add(keras.layers.InputLayer(input_shape=(24, 1)))
# Hidden layer
model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=64)))
model.add(keras.layers.Dense(1))
#Compile model
model.compile(optimizer='adam', loss='mse')

model.summary()

model.compile(loss='mse',
              optimizer='adam',
              metrics=['mae'])

#---------------#
# train         #
#---------------# 

history = model.fit(x=trainData_x, y=trainData_y,
                    validation_data=(testData_x, testData_y),
                    epochs=25)

#---------------#
# save          #
#---------------#

# network_storage is a path, we just want the directory name here
model.save(network_storage)
