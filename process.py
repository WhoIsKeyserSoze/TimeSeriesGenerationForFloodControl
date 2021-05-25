import timeSeries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
import pmdarima as pm
from pmdarima.arima import auto_arima
import warnings
warnings.filterwarnings('ignore')

def arma_process(df, d):
    # df=df[:int(0.7*(len(df)))]
    col = 'height'
    if d > 0 :
        col = 'height_diff'
    plot_acf(df[col].iloc[1:],lags=25)
    plt.show()
    p = int(input("p = "))
    plot_pacf(df[col].iloc[1:],lags=24)
    plt.show()
    q = int(input("q = "))
    print("p = ", p, " q = ", q)
    model=ARMA(df[col].dropna(),order=(p,q))
    model_fit = model.fit()
    print(model_fit.summary())
    start_date = df.index[int(0.5*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[int((len(df))-1)]
    print("End date : ",end_date)
    df['ARMA_forecast'] = model_fit.predict(start= start_date, end= end_date, dynamic=True)
    df[[col, 'ARMA_forecast']].plot(figsize=(10, 5))
    plt.title('ARMA Forecast vs Real Data')
    plt.show()

    return df['ARMA_forecast']

# def autoarima_process(df):
#     df=df[:int(0.7*(len(df)))]
#     #dividing into train and test
#     train = df[:int(0.5*(len(df)))]
#     test = df[int(0.5*(len(df))):]
#     train['height'].plot()
#     test['height'].plot()
#     plt.show()
#
#     model = pm.auto_arima(train, seasonal = True, m = 8)
#     forecast = model.predict(test.shape[0])
#     df['height'].plot(figsize=(10,5))
#     forecast.plot()
#     plt.show()

def arima_process(df, d):
    # df=df[:int(0.7*(len(df)))]
    col = 'height'
    if d > 0 :
        col = 'height_diff'
    plot_acf(df[col].iloc[1:],lags=25)
    plt.show()
    p = int(input("p = "))
    plot_pacf(df[col].iloc[1:],lags=24)
    plt.show()
    q = int(input("q = "))
    print("p = ", p, " q = ", q)
    model1=ARIMA(df[col].dropna(),order=(p,d,q))
    model_fit1=model1.fit()
    start_date = df.index[int(0.5*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[int((len(df))-1)]
    df['forecast_ARIMA'] = model_fit1.predict(start = start_date, end= end_date, dynamic= True)
    df[[col, 'forecast_ARIMA']].plot(figsize=(10, 5))
    plt.title('ARIMA Forecast vs Real Data')
    plt.show()

    return df['forecast_ARIMA']

def sarima_process(df, d):
    col = 'height'
    if d > 0 :
        col = 'height_diff'
    plot_acf(df[col].iloc[1:],lags=25)
    plt.show()
    p = int(input("p = "))
    plot_pacf(df[col].iloc[1:],lags=24)
    plt.show()
    q = int(input("q = "))
    print("p = ", p, " q = ", q)
    # timeSeries.analyse_data(df)
    # m = int(input("m = "))
    m = 60
    model=sm.tsa.statespace.SARIMAX(df[col],order=(p,d,q),seasonal_order=(p,d,q,m))
    result=model.fit()
    start_date = df.index[int(0.5*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[int((len(df))-1)]
    df['forcast_SARIMA']=result.predict(start= start_date, end= end_date, dynamic=True)
    df[[col,'forcast_SARIMA']].plot(figsize=(10, 5))
    plt.title('SARIMA Forecast vs Real Data')
    plt.show()
    return df['forcast_SARIMA']

def autoarima(data):

   #Displaying basic data
   data.plot()

   #Test on the st if it is stationary
   # isStatio = gptest.checkForStationarity(data)

   #decomposition
   #result = seasonal_decompose(data,model='additive',period=2)
   #fig = result.plot()
   #plt.plot(fig)

   #train and test datasets to build model
   train = data.loc[:data.index[int(0.5*(len(data)))]]
   test = data.loc[data.index[int(0.5*(len(data)))]:]

   #Building Auto ARIMA model
   stepwise_model = auto_arima(train, start_p=1, d=1, start_q=1,
                           max_p=3, max_q=3, start_P=1,
                           D=1, start_Q=1, max_P=3, max_D=3,
                           max_Q=5, m=2, seasonal = True,
                           error_action='ignore',trace = True,
                           suppres_warnings=True,stepwise = True,
                           random_state=20,n_fits = 50 )
   print(stepwise_model.aic())


   #Train the Model
   stepwise_model.fit(train)

   #Forecasting on the test data
   future_forecast = pd.DataFrame(stepwise_model.predict(n_periods=2976), index=test.index)
   future_forecast.columns = ['Predictions']
   pd.concat([test,future_forecast],axis=1).plot()
   pd.concat([train,future_forecast],axis=1).plot()

   # This returns an array of predictions:
   print(future_forecast)


   #Final Display
   plt.figure(figsize=(10,10))
   plt.plot(train,label='Training')
   plt.plot(test,label='Test')
   plt.plot(future_forecast,label='Predicted')
   plt.legend(loc='upper left')
   plt.title('AUTO-ARIMA Forecast vs Real Data')
   plt.show()

   return future_forecast
