import datetime
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

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

    return df, isStationary

def analyse_data(df):
    # df.sort_index(inplace=True)
    res = seasonal_decompose(df['height'], model='multiplicative', period = 60)
