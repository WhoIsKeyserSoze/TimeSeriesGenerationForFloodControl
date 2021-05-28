from sklearn.metrics import r2_score
from math import sqrt
import  numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error




#Root Mean Squared Error
def rmse(actual,forecast):
    return sqrt(mean_squared_error(actual, forecast))

#Mean Absolute Error
def mae(actual,forecast):
   return mean_absolute_error(actual, forecast)

#Mean Squared Error
def mse(actual, forecast):
    return mean_squared_error(actual, forecast)

#Mean Absolute Percentage Error
def mape(actual, pred): 
    actual, pred = np.array(actual), np.array(pred)

    for i in ragne(0, )


    return np.mean(np.abs((actual - pred) / actual)) * 100

#Coefficient Of Determination
def r2score(test,forecast):
    return r2_score(test, forecast)

