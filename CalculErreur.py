from sklearn.metrics import r2_score
from math import sqrt
import  numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error




#Root Mean Squared Error
def rmse(test,future_forecast):
    return sqrt(mean_squared_error(test,future_forecast))

#Mean Absolute Error
def mae(test,future_forecast):
   return mean_absolute_error(test,future_forecast)

#Mean Squared Error
def mse(test,future_forecast):
    return mean_squared_error(test, future_forecast)

#Mean Absolute Percentage Error
def mape(actual, pred): 
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs((actual - pred) / actual)) * 100

#Coefficient Of Determination
def r2score(test,future_forecast):
    return r2_score(test,future_forecast)

