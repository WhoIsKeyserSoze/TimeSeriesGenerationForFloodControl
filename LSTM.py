import datetime
from tensorflow import keras
import numpy
from LSTM_module import LSTMdata
import dataGeter

model_path = r".\LSTM_module\network_storage"


# returns a measure_list contening the model's prediction
# makes 'pre_len' value prediction
# a measure_list is a list of tuple (datetime.datetime, float)
def PredictFromList(measure_list, pred_len) :

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
    
    # load model
    model = keras.models.load_model(model_path)
    predictions = []

    for i in range(0, pred_len):
        pred = model.predict(numpy.array([value_list[-24:]]))
        value_list.append([pred[0][0]])
        predictions.append(pred[0][0])

    predictions = LSTMdata.un_normalize_array(numpy.array(predictions), minV, maxV)

    # add dates
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
    
