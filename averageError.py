import dataGeter
import random
import datetime
from math import sqrt

import numpy as np
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Returns a list of n timeseries (list of tuple(date, float))
def GetRandomTimeSeries(n) :
    # first get a list of all sensors code
    sensorList = dataGeter.GetAllActivesSensors()
    nbSensors = len(sensorList)
    # will serve as a base date to generate random date from a month ago to now
    monthAgo = datetime.datetime.now() - datetime.timedelta(days=30)
    monthAgo = datetime.date(monthAgo.year, monthAgo.month, monthAgo.day)

    i = 0
    stList = []
    while(i < n):
        randomDate = monthAgo + datetime.timedelta(days=random.randint(1, 28))
        randomSensor = sensorList[random.randint(0, nbSensors)]
        ts = dataGeter.GetMeasures(randomDate, 2, randomSensor)
        # Sometimes datageter doesn"t fine any
        if(len(ts) == 48):
            stList.append(ts)
            i += 1
    
    return stList

# used to prepare date for error calculation
# we need a list of timeseries to make prediction on
# and a list of timeseries to compare the prediction with

# takes a list of timeseries (list of tuple(date, float))
# will cut each timeseries to make a data_len timeseries (to give to the prediction function)
# and a pre_len timeseries to compare the prediction with
def CutTimeSeries(tsList, data_len, pre_len) :
    #check len
    if(len(tsList[0]) < data_len + pre_len) :
        Warning.warn("timeSeriesGenerator.error : timeseries's len is too short") 
        return ([], [])
    
    data, pred = [], []

    for ts in tsList :
        data.append(ts[:data_len])
        pred.append(ts[data_len: data_len+pre_len])

    return data,pred


#Root Mean Squared Error
def rmse(actual_values, forecast):
    return sqrt(mean_squared_error(actual_values, forecast))

#Mean Absolute Error
def mae(actual_values, forecast):
   return mean_absolute_error(actual_values, forecast)

#Mean Squared Error
def mse(actual_values, forecast):
    return mean_squared_error(actual_values, forecast)

#Mean Absolute Percentage Error
def mape(actual_values, forecast):
    actual_values, forecast = np.array(actual_values), np.array(forecast)
    return np.mean(np.abs((actual_values - forecast) / actual_values)) * 100

#Coefficient Of Determination
def r2score(actual_values, forecast):
    return r2_score(actual_values, forecast)

# takes 2 list of measurse list( (date, float) )
def error(actual, forecast) :
    # converts measure list into value array
    # just cuting date value from each tuple
    for i in range(len(actual)) :
        actual[i] = actual[i][1]
        forecast[i] = forecast[i][1]

    actual, forecast = np.array(actual), np.array(forecast)

    rmse = sqrt(mean_squared_error(actual, forecast))
    mae = mean_absolute_error(actual, forecast)
    mse = mean_squared_error(actual, forecast)
    mape = np.mean(np.abs((actual - forecast) / actual)) * 100
    r2score = r2_score(actual, forecast)

    return [rmse, mae, mse, mape, r2score]

def ComputeMetrics(tsData, tsPred, tsReal) :
    
    total = len(tsReal)
    # [rmse, mae, mse, mape, r2score]
    metrics = [0,0,0,0,0]

    for i in range(0, len(tsData)):
        errors = error(tsReal[i], tsPred[i])
        for j in range(len(metrics)):
            metrics[j] += errors[j]
        total += 1

    for k in range(len(metrics)):
        metrics[k] = metrics[k] / total

    return metrics
