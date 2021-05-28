import datetime
import os
from sklearn import metrics
# removes tensor flow information
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
# 0 : infos warnings error
# 1 : warnings error
# 2 : errors
# 3 : nothing

from tensorflow import keras
import numpy
from LSTM_module import LSTMdata
import dataGeter
import averageError as ae

model_path = r".\LSTM_module\network_storage"
model = 'notloaded'
isLoaded = False


# returns a measure_list contening the model's prediction
# makes 'pre_len' value prediction
# a measure_list is a list of tuple (datetime.datetime, float)

# If the measure_list does not make at least 24 measures, the LSTM network won't be able to make predictions
def PredictFromList(measure_list, pred_len) :

    #checking measure_list size
    if(len(measure_list) < 24) :
        Warning.warn("TimeSeriesGenerator.LSTM.PredictFromList : Not enought data. Make sure to give at least 24 measures")
        return []

    # data convertion section 
    # this algo doesn't need date to make prediction
    value_list = []
    for measure in measure_list :
        value_list.append([measure[1]])
    # But it needs normalised data
    value_list,minV, maxV = LSTMdata.normalize_array(numpy.array(value_list))
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
    predictions = LSTMdata.un_normalize_array(numpy.array(predictions), minV, maxV)

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
