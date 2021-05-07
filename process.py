import timeSeries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
import warnings
warnings.filterwarnings('ignore')

def arma_process(df, d):
    # df=df[:int(0.7*(len(df)))]
    col = 'height'
    if d > 0 :
        col = 'height_diff'
    plot_acf(df[col].iloc[1:],lags=30)
    plt.show()
    p = int(input("p = "))
    plot_pacf(df[col].iloc[1:],lags=30)
    plt.show()
    q = int(input("q = "))
    print("p = ", p, " q = ", q)
    model=ARMA(df[col].dropna(),order=(p,q))
    model_fit = model.fit()
    print(model_fit.summary())
    start_date = df.index[int(0.5*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[-1]
    print("End date : ",end_date)
    df['ARMA_forecast'] = model_fit.predict(start= start_date, end= end_date, dynamic=True)
    df[[col, 'ARMA_forecast']].plot(figsize=(10, 5))
    plt.title('ARMA Forecast vs Real Data')
    plt.show()

def autoarima_process(df):
    df=df[:int(0.7*(len(df)))]
    #dividing into train and test
    train = df[:int(0.5*(len(df)))]
    test = df[int(0.5*(len(df))):]
    train['height'].plot()
    test['height'].plot()
    plt.show()

    model = pm.auto_arima(train, seasonal = True, m = 8)
    forecast = model.predict(test.shape[0])
    df['height'].plot(figsize=(10,5))
    forecast.plot()
    plt.show()

def arima_process(df, d):
    # df=df[:int(0.7*(len(df)))]
    col = 'height'
    if d > 0 :
        col = 'height_diff'
    plot_acf(df[col].iloc[1:],lags=30)
    plt.show()
    p = int(input("p = "))
    plot_pacf(df[col].iloc[1:],lags=30)
    plt.show()
    q = int(input("q = "))
    print("p = ", p, " q = ", q)
    model1=ARIMA(df[col].dropna(),order=(p,d,q))
    model_fit1=model1.fit()
    start_date = df.index[int(0.5*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[-1]
    df['forecast_ARIMA'] = model_fit1.predict(start = start_date, end= end_date, dynamic= True)
    df[[col, 'forecast_ARIMA']].plot(figsize=(10, 5))
    plt.title('ARIMA Forecast vs Real Data')
    plt.show()
