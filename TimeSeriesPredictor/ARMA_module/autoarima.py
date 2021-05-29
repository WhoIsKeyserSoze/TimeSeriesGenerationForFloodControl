from . import armaData
from pmdarima.arima import auto_arima
import warnings
import pandas as pd

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
