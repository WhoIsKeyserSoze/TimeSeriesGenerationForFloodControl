import warnings
import pandas as pd

from statsmodels.tsa.arima_model import ARMA


from . import armaData

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
    
    p = 1
    q = 1

    model=ARMA(df['height'].dropna(),order=(p,q))

    model_fit = model.fit(disp=0)

    # prepare res (dataframe)

    # prepare date column
    start_date = df['date'].iloc[-1]
    delta = start_date - df['date'].iloc[-2]
    dates = []
    for i in range(0, pre_len+p) :
        dates.append(start_date + (i) * delta)
    
    res = pd.DataFrame(dates)

    res['predValue'] = model_fit.predict(start= p, end= pre_len+p, dynamic=True)
    res.columns = ['date', 'predValue']
    return res[p:]
