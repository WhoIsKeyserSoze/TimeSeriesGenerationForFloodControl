from matplotlib.colors import Normalize
import randomDataGeter as rdg
from tensorflow import keras
import numpy
import matplotlib.pyplot as plt

#---------------#
# Prepare data  #
#---------------# 

data_path = r"D:\Desktop\Prog\L3\BE\WorkBench\random_data_storage"

trainning_proportion = 0.85
nb_rawSeries = 30
rawSeries_len = 29*24 #29 days and 24 hours of measurments

# First donwload tons of measures from hubeau api's
# if already done, comment next line of code

# rdg.random_data_geter(nb_rawSeries, data_path, period=rawSeries_len)

# then load them into a nice list

rawData = rdg.load_data(data_path, rawSeries_len)
rawData = rdg.normalize_dataset(rawData)

#note : min and max value will serv to un-normalize the prediction from the NN

# making many nb_day long time series from the raw data
dataset = rdg.timeSeriesGenerator(rawData, rawSeries_len, 24)

p = int(trainning_proportion * dataset[0].size)
trainData_x = dataset[0][:p]
trainData_y = dataset[1][:p]

testData_x = dataset[1][p:]
testData_y = dataset[1][p:]

#---------------#
# prepare model #
#---------------#

model = keras.models.Sequential()
model.add(keras.layers.InputLayer(input_shape=(24, 1)))
# model.add( keras.layers.GRU(200, dropout=.1, recurrent_dropout=0.5, return_sequences=False, activation='relu') )
model.add(keras.layers.GRU(128))
model.add(keras.layers.Dense(1))

model.summary()

model.compile(loss='mse',
              optimizer='adam',
              metrics=['mae'])

#---------------#
# train         #
#---------------# 

history = model.fit(x=trainData_x, y=trainData_y,
                    validation_data=(testData_x, testData_y),
                    epochs=25,
                    shuffle=True,
                    batch_size=25)

#---------------#
# test          #
#---------------#

# model is the neural network, base_seq a list of measurements and pred_len is the size of the output list
def predict(model, base_seq, pred_len) :
    seq_len = len(base_seq)
    pred_seq = [base_seq[-1][0]]

    for i in range(0, pred_len):
        pred = model.predict(numpy.array([base_seq[-1*seq_len:]]))
        base_seq.append([pred[0][0]])
        pred_seq.append(pred[0][0])
    
    return pred_seq


st = rdg.load_file(data_path,
                   '2021-04-20_U060001001.csv', 0)
st, minST, maxST = rdg.normalize_array(st)

context_size = 50
sub_seq_start = 100
prediction_len = 24
sub_seq_len = 24 + prediction_len



sub_seq = []
for i in range(0, sub_seq_len):
    sub_seq.append([st[sub_seq_start+i][0]])
pred = predict(model, sub_seq[:24], prediction_len)

x = numpy.arange(sub_seq_start-context_size, sub_seq_start+sub_seq_len+context_size)
plt.plot(x, st[sub_seq_start-context_size: sub_seq_start +
         sub_seq_len+context_size], color='blue')

x = numpy.arange(sub_seq_start, sub_seq_start+sub_seq_len)
plt.plot(x, sub_seq, color='green')

x = numpy.arange(sub_seq_start+sub_seq_len - prediction_len-1,
                 sub_seq_start+sub_seq_len)
plt.plot(x, pred, color='red')

plt.show()


#---------------#
# save          #
#---------------#


if(str(input()) == 'yes') :
    print("saved")

print('Done.\nExit programme.')
