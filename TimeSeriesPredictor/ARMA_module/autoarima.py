from pmdarima.arima import auto_arima
import warnings
import pandas as pd
import datetime


from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from .. import averageError as ae
from .. import dataGeter

import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',
                        FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',
                        FutureWarning)


def PredictFromList(measures_list, pre_len):
    df = pd.DataFrame(measures_list)
    df.columns = ['date', 'height']




    
    pred = PredictFromDF(df, pre_len)

    pred = pred.values.tolist()
    res = []

    for i in range(0, len(pred)):
        res.append((pred[i][0], pred[i][1]))

    return res


def PredictFromDF(df, pre_len):

    model = auto_arima(df['height'], start_p=1, d=1, start_q=1,
                       max_p=3, max_q=3, start_P=1,
                       D=1, start_Q=1, max_P=3, max_D=3,
                       max_Q=5, m=2, seasonal=True,
                       error_action='ignore', trace=True,
                       suppres_warnings=True, stepwise=True,
                       random_state=20, n_fits=50)

    model.fit(df['height'])

    pred = model.predict(n_periods=pre_len)

    # prepare res (dataframe)

    # prepare date column
    start_date = df['date'].iloc[-1]
    delta = start_date - df['date'].iloc[-2]
    dates = []
    for i in range(0, pre_len):
        dates.append(start_date + (i+1) * delta)

    res = pd.DataFrame(dates)

    res['predValue'] = pred
    res.columns = ['date', 'predValue']
    return res

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
