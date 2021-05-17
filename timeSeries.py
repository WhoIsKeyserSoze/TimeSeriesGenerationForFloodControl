import donnees
import datetime
import graph
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose



#graph.show_measures(height_measures, flow_measures)

# Puts the data into a pandas DataFrame from API hydro-eau eaufrance
def getDataFrameFromApi (start_date, duration, sensor_code, height, flow) :
    height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
    flow_measures = donnees.get_measures(start_date, duration, sensor_code, flow)
    df = pd.DataFrame(height_measures, columns = ['date','height'])
    df['date'] = pd.to_datetime(df.date)
    df.set_index('date', inplace=True)
    df.sort_values(by='date', inplace = True)
    # print(df.head())
    return df

def getDataFromCsv():
   data=pd.read_csv('Export_SerieHydro_LUCHON.csv',header=1, parse_dates=['Date (TU)'],index_col='Date (TU)', dayfirst = True)
   #Delete the columns Qualification Contuinité and Méthode
   data=data.drop(['Qualification','Continuité','Méthode'],1)


   #Rename the columns Date (TU) and Valeur (mm)
   # data = data.set_index('Date (TU)').asfreq('15T')
   data.index = pd.to_datetime(data.index)
   data.rename(columns={'Valeur (mm)': 'height'}, index={'Date (TU)' : 'date' }, inplace = True)
   data.index.names=['date']
   # data.index.freq='15T'
   print(data.index)


   print(data.head())
   return data

def plotTheData(df):
    df.plot()
    plt.show()

# Check for stationarity
def checkForStationarity(x):
    stationary = False
    print("\n-------------------------------------------------------")
    print("Check for stationarity")
    print("-------------------------------------------------------")
    print("Null Hypothesis : Non stationarity exists in the serie")
    print("Alternative Hypothesis : Data is stationary")
    print("-------------------------------------------------------")
    result = adfuller(x)
    print("Result : ",result)
    print("\n")
    print("We take 95% confidence level, We check if result[1] <= 0.05 (5%) : ")
    print("-------------------------------------------------------")
    if result[1]<= 0.05 :
        stationary = True
        print("Result[1] = ", result[1], " <= 0.05 \nFail to reject null hypothesis\nData is Stationary")
    else :
        print("Result[1] = ", result[1], " > 0.05 \nReject null hypothesis\nThere is Non Stationarity in the serie")
    print("-------------------------------------------------------")
    return stationary

# Plots the AutoCorrelationFunction ans the PartialAutoCorrelationFunction
def plotAcfAndPacf(df):
    # plots the acf
    acf_plot = plot_acf(df.height, lags=96)
    plt.show()

    pacf_plot = plot_pacf(df.height)
    plt.show()

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
    plotTheData(df)
    return df,dif

def analyse_data(df):
    # df.sort_index(inplace=True)
    res = seasonal_decompose(df['height'], model='multiplicative', period = 60)
    res.plot()
    plt.show()
