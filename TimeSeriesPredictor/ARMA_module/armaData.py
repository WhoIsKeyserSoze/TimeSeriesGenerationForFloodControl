import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

import datetime
from .. import averageError as ae

# Check for stationarity
def checkForStationarity(x):
    stationary = False
    result = adfuller(x)
    if result[1] <= 0.05:
        stationary = True
    return stationary

def stationarize(df, iterMax):
    # stationarisation
    isStationary = False
    dif = 0
    i = 0
    while (not isStationary and i<iterMax) :
        dif += 1
        #Y(t) = Y(t)-Y(t-1)
        df['height'] = df['height'] - df['height'].shift(dif)
        isStationary = checkForStationarity(df['height'].dropna())

    return df, dif

def analyse_data(df):
    # df.sort_index(inplace=True)
    res = seasonal_decompose(df['height'], model='multiplicative', period = 60)
