import warnings
import pandas as pd

import statsmodels.api as sm


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
    d = 1
    m = 60

    isStatio = armaData.checkForStationarity(df['height'])
    if(not isStatio):
        print("The timeseries is not stationary, try to stationarise it...")
        df, isStatio = armaData.stationarize(df, 10)
        if(not isStatio):
            print("The timeseries is not stationary, return no predictions")
            return []
        else:
            print("sucess")

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
