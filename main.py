import timeSeries
import process
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Parameters for getting data from api
start_date = datetime.date(2021, 4, 7)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'

# Main

#With Data from Api
# df = timeSeries.getDataFrameFromApi(start_date, duration, sensor_code, height, flow)
# timeSeries.plotTheData(df)
# isStationary = timeSeries.checkForStationarity(df['height'])
# d = 0
# if isStationary :
#     # Execution of arma
#     print("Execution of arma")
# else :
#     # Transmormation to stationary
#     print("Transformation to stationary")
#     diff, d = timeSeries.stationarize(df)
#     print("diff : ",diff.head())
#     print("parameter d : ",d)
#     print("Execution of arma")
#     process.arma_process(diff,d)
#     print("Execution of ARIMA")
#     process.arima_process(diff, d)


# #With data from Csv file
df2 = timeSeries.getDataFromCsv()
timeSeries.plotTheData(df2)
# timeSeries.analyse_data(df2)
isStationary = timeSeries.checkForStationarity(df2['height'])
if isStationary :
    d = 0
    # Execution of arma
    print("Execution of arma")
    arma = process.arma_process(df2,d)
    # print("Execution of auto_arima")
    # process.autoarima_process(df2)
    print("Execution of ARIMA")
    arima = process.arima_process(df2, d)

    print("Execution of sarima")
    sarima = process.sarima_process(df2, d)

    # print("Execution of auto arima")
    # aarima = process.autoarima(df2['height'])

    plt.plot(figsize=(10, 5))
    plt.plot(df2['height'], label= 'Real Data')
    plt.plot(arma,label='Arma Forecast')
    plt.plot(arima,label='Arima Forecast')
    plt.plot(sarima,label='Sarima Forecast')
    # plt.plot(aarima,label='Auto-Arima Forecast')
    plt.title('Forecast vs Real Data')
    plt.legend()
    plt.show()
else :
    # Transmormation to stationary
    print("Transformation to stationary")
