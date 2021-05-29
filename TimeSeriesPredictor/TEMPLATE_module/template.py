#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   THIS IS A TEMPLATE YOU NEED TO MODIFY TO ADD A NEW NEURAL NETWORK ALGORITHM !   #
#         Follow the following instructions to complete this template well.         #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# The lines you need to modify will be flaged by for example : #3#                  #
#                                                                                   #   
# ALGO = your algorithm name                                                        #
#                                                                                   #
# After naming your algorithm (like LSTM, GRU, BILSTM...), you can modify the code  #
#                                                                                   #
# * Line 38 : LSTMdata -> ALGOdata                                                  #
# * Line 50 : 8 -> Length of your algorithm name + 4 (example LSTM -> 4+4 = 8)      #
# * Line 50 : LSTM_storage -> ALGO_storage                                          #
# * Line 64 : LSTM -> ALGO                                                          #
# * Line 73 : LSTMdata -> ALGOdata                                                  #
# * Line 95 : LSTMdata -> ALGOdata                                                  #
# * Lines 60, 64, 65, 92, 128 : 24 -> Number of measures your algorithm takes as    #
#                                                                         input     #
#   WARNING : If you modify the number of measures your algorithm takes, don't      #  
#   forget to modify it in the templatedata.py as well.                             #
#                                                                                   #
# Don't forget to delete all the flags #?#                                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import datetime
import os
import platform
import warnings

from sklearn import metrics
# removes tensor flow information
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
# 0 : infos warnings error
# 1 : warnings error
# 2 : errors
# 3 : nothing

from tensorflow import keras
import numpy
from . import templateData   #1#
from .. import dataGeter
from .. import averageError as ae

os = platform.system()
if(os == "Linux"):
    separator = '/'
elif(os == "Windows"):
    separator = '\\'
else:
    warnings.warn("OS not supported, get the fuck out of my library with your shitty OS! You trash, go DL Windows or Linux! è.é")

model_path = __file__[:-8] + separator + "LSTM_storage"  #2# #3#
model = 'notloaded'
isLoaded = False


# returns a measure_list contening the model's prediction
# makes 'pre_len' value prediction
# a measure_list is a list of tuple (datetime.datetime, float)

# If the measure_list does not make at least 24 measures, the network won't be able to make predictions  #4#
def PredictFromList(measure_list, pred_len) :

    #checking measure_list size
    if(len(measure_list) < 24) :
        warnings.warn("TimeSeriesGenerator.LSTM.PredictFromList : Not enought data. Make sure to give at least 24 measures") #5# #6#
        return []

    # data convertion section 
    # this algo doesn't need date to make prediction
    value_list = []
    for measure in measure_list :
        value_list.append([measure[1]])
    # But it needs normalised data
    value_list, minV, maxV = templateData.normalize_array(
        numpy.array(value_list))  # 7#
    temp = []
    for value in value_list :
        temp.append([value[0]])
    value_list = temp
    

    # Prediction section
    # load model
    global model
    global isLoaded
    if( not isLoaded) : 
        model = keras.models.load_model(model_path)
        isLoaded = True

    predictions = []
    # predicts
    for i in range(0, pred_len):
        pred = model.predict(numpy.array([value_list[-24:]]))
        value_list.append([pred[0][0]])
        predictions.append(pred[0][0])
    # unormalise predictions
    predictions = templateData.un_normalize_array(
        numpy.array(predictions), minV, maxV)  # 8#

    # convert prediction to list of (date, float)
    # we have float, just need to add dates to them
    result = []
    start_date = measure_list[-1][0]
    for i in range(0, pred_len):
        date = start_date + datetime.timedelta(hours=i+1)
        result.append((date, predictions[i]))
    
    return result

# sensor_code is a string, pre_len is a int, startdate a datetie.datetime
# Return a prediction from now of pre_len values from the sensor
# if a date is spécified, it will return the prediction starting at the star_date
def PredictFromSensor(sensor_code, pre_len, pred_starting_date=0) :
    if(pred_starting_date == 0):
        measures = dataGeter.GetLastMeasures(sensor_code)
        return PredictFromList(measures, pre_len)
    else :
        start_date = pred_starting_date - datetime.timedelta(days=1)
        measures = dataGeter.GetMeasures(start_date, 1, sensor_code)
        return PredictFromList(measures, pre_len)


# return a list of metrics calculated
# [rmse, mae, mse, mape, r2score]
# pre_len is the size of prediction
# data_size is the number of timeseries used to make the average
def ComputeError(pre_len, data_size) :
    print("Error computing will take few minutes...")
    data = ae.GetRandomTimeSeries(data_size)
    tsData, tsReal = ae.CutTimeSeries(data, 24, pre_len)
    
    tsPred = []
    for ts in tsData :
        tsPred.append(PredictFromList(ts, pre_len))

    return ae.ComputeMetrics(tsData, tsPred, tsReal)
