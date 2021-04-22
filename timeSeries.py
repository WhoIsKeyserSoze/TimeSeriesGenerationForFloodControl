import donnees
import datetime
import graph
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

start_date = datetime.date(2021, 4, 7)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'



#graph.show_measures(height_measures, flow_measures)

# Puts the data into a pandas DataFrame from API hydro-eau eaufrance
def getDataFrameFromApi (duration, sensor_code, height, flow) :
    height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
    flow_measures = donnees.get_measures(start_date, duration, sensor_code, flow)
    df = pd.DataFrame(height_measures, columns = ['date','height'])
    df['date'] = pd.to_datetime(df.date)
    df.set_index('date', inplace=True)
    # print(df.head())
    return df


# Check for stationarity
def checkForStationarity(df):
    stationary = False
    print("\n-------------------------------------------------------")
    print("Check for stationarity")
    print("-------------------------------------------------------")
    print("Null Hypothesis : Non stationarity exists in the serie")
    print("Alternative Hypothesis : Data is stationary")
    print("-------------------------------------------------------")
    x = df['height']
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



# Main
df = getDataFrameFromApi(duration, sensor_code, height, flow)
isStationary = checkForStationarity(df)
if isStationary :
    # Execution of arma
    print("Execution of arma")
else :
    # Transmormation to stationary
    print("Transformation to stationary")
# plotAcfAndPacf(df)
