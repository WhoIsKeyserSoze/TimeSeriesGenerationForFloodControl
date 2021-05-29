import datetime
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

# Check for stationarity
def checkForStationarity(x):
    res = adfuller(x)
    ADF = res[0]
    pValue = res[1]
    return (ADF < 0 and pValue < 0.05)

def stationarize(df):
    # stationarisation
    isStationary = False
    dif = 0
    while (not isStationary):
        dif += 1
        #Y(t) = Y(t)-Y(t-1)
        df['height_diff'] = df['height'] - df['height'].shift(dif)
        isStationary = checkForStationarity(df['height_diff'].dropna())

    print("Data is now stationarized using (", dif,") difference")
    return df,dif

def analyse_data(df):
    # df.sort_index(inplace=True)
    res = seasonal_decompose(df['height'], model='multiplicative', period = 60)
