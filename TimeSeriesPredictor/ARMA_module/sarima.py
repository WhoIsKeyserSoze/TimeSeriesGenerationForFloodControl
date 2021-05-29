import warnings
import pandas as pd

import statsmodels.api as sm

import datetime
from .. import dataGeter
from .. import averageError as ae


from . import armaData


def PredictFromList(measures_list, pre_len):
    df = pd.DataFrame(measures_list)
    df.columns = ['date', 'height']

    #check coeff
    coeff = armaData.checkForStationarity(df['height'])
    if (coeff):
        warnings.warn(
            "TimeSeriesPredictor.arma : stationarity coefficient is to high, returning no predictions")
        return []

    pred = PredictFromDF(df, pre_len)
    pred = pred.values.tolist()
    res = []

    for i in range(0, len(pred)):
        res.append((pred[i][0], pred[i][1]))

    return res


def PredictFromDF(df, pre_len):

    p = 1
    q = 1
    df,d = armaData.stationarize(df,100)
    m = 60

    model = sm.tsa.statespace.SARIMAX(df['height'].dropna(), order=(
        p, d, q), seasonal_order=(p, d, q, m))

    model_fit = model.fit(disp=0)

    # prepare res (dataframe)
    # prepare date column
    start_date = df['date'].iloc[-1]
    delta = start_date - df['date'].iloc[-2]
    dates = []
    for i in range(0, pre_len+p):
        dates.append(start_date + (i) * delta)

    res = pd.DataFrame(dates)

    res['predValue'] = model_fit.predict(start=p, end=pre_len+p, dynamic=True)
    res.columns = ['date', 'predValue']
    return res[p:]

# sensor_code is a string, pre_len is a int, startdate a datetie.datetime
# Return a prediction from now of pre_len values from the sensor
# if a date is spécified, it will return the prediction starting at the star_date
def PredictFromSensor(sensor_code, pre_len, pred_starting_date=0):
    if(pred_starting_date == 0):
        measures = dataGeter.GetLastMeasures(sensor_code)
        return PredictFromList(measures, pre_len)
    else:
        start_date = pred_starting_date - datetime.timedelta(days=5)
        measures = dataGeter.GetMeasures(start_date, 5, sensor_code)
        return PredictFromList(measures, pre_len)


# return a list of metrics calculated
# [rmse, mae, mse, mape, r2score]
# pre_len is the size of prediction
# data_size is the number of timeseries used to make the average
def ComputeError(pre_len, data_size):
    print("Error computing will take few minutes...")
    data = ae.GetRandomTimeSeries(data_size)
    tsData, tsReal = ae.CutTimeSeries(data, 24, pre_len)

    tsPred = []
    for ts in tsData:
        tsPred.append(PredictFromList(ts, pre_len))

    return ae.ComputeMetrics(tsData, tsPred, tsReal)
