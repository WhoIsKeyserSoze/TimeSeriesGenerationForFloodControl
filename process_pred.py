import timeSeries
import pandas as pd
import CalculErreur
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
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    start_date = df.index[int(0.12*(len(df)))]
    print("Start date : ",start_date)
    end_date = df.index[int(0.9*(len(df)))]
    print("End date : ",end_date)
    df['ARMA_forecast'] = model_fit.predict(start= start_date, end= end_date, dynamic=True)
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan,0, inplace=True)
    return df
   


def arima_process(df, d):
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
    model_fit1=model1.fit(disp=0)
    start_date = df.index[int(0.12*(len(df)))]
    end_date = df.index[int(0.3*(len(df)))]
    df['forecast_ARIMA'] = model_fit1.predict(start = start_date, end= end_date, dynamic= True)
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan,0, inplace=True)
    return df
   

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
    m = 60
    model=sm.tsa.statespace.SARIMAX(df[col],order=(p,d,q),seasonal_order=(p,d,q,m))
    result=model.fit(disp=0)
    start_date = df.index[int(0.12*(len(df)))]
    end_date = df.index[int(0.3*(len(df)))]
    df['forcast_SARIMA']=result.predict(start= start_date, end= end_date, dynamic=True)
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan,0, inplace=True)
    return df

def modele_train(test,train):
    #Building Auto ARIMA model
    stepwise_model = auto_arima(train, start_p=1, d=1, start_q=1,
                           max_p=3, max_q=3, start_P=1, 
                           D=1, start_Q=1, max_P=3, max_D=3,
                           max_Q=5, m=2, seasonal = True,
                           error_action='ignore',trace = True,
                           suppres_warnings=True,stepwise = True,
                           random_state=20,n_fits = 50 )
    #Train the Model
    stepwise_model.fit(train)
    return stepwise_model
      
def forcasting_mesure(test,train,stepwise_model):
   #Forecasting on the test data
   future_forecast = pd.DataFrame(stepwise_model.predict(n_periods=2976), index=test.index)
   future_forecast.columns = ['Predictions']
   pd.concat([test,future_forecast],axis=1).plot()
   pd.concat([train,future_forecast],axis=1).plot()
   l*pred=list()
   for i in future_forecast['Predictions']:
       pred.append(i)
   return pred
   

       
def final_display(train,test,future_forecast):   
   #Final Display
   data=timeSeries.getDataFromCsv()
   data.plot()
   plt.grid(True)
   plt.figure(figsize=(10,10))
   plt.plot(train,label='Training')
   plt.plot(test,label='Test')
   plt.plot(future_forecast,label='Predicted')
   plt.legend(loc='upper left')
   plt.show()


   
    
def predict_arma(measure_liste,len_liste):
  d=0
  df = pd.DataFrame(measure_liste)
  df.columns = ['date', 'height']
  print(df.columns)
  predictions = arma_process(df,d)
  pred = predictions.values.tolist()
  res=[]
  for i in range(0,len(pred)):
      res.append((pred[i][0],pred[i][2]))
  return res
    

def predict_arima(measure_liste,len_liste):
  d=0
  df = pd.DataFrame(measure_liste)
  df.columns = ['date', 'height']
  print(df.columns)
  predictions = arima_process(df,d)
  pred = predictions.values.tolist()
  res=[]
  for i in range(0,len(pred)):
      res.append((pred[i][0],pred[i][2]))  
  return res

def predict_sarima(measure_liste,len_liste):
  d=0
  df = pd.DataFrame(measure_liste)
  df.columns = ['date', 'height']
  print(df.columns)
  predictions = sarima_process(df,d)
  pred = predictions.values.tolist()
  res=[]
  for i in range(0,len(pred)):
      res.append((pred[i][0],pred[i][2]))    
  return res
    
    
    