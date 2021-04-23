import timeSeries
import pandas as pd
import datetime

# Parameters for getting data from api
start_date = datetime.date(2021, 4, 7)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'

# Main

#With Data from Api
df = timeSeries.getDataFrameFromApi(start_date, duration, sensor_code, height, flow)
timeSeries.plotTheData(df)
isStationary = timeSeries.checkForStationarity(df)
if isStationary :
    # Execution of arma
    print("Execution of arma")
else :
    # Transmormation to stationary
    print("Transformation to stationary")

#With data from Csv file
df2 = timeSeries.getDataFromCsv()
timeSeries.plotTheData(df2)
isStationary = timeSeries.checkForStationarity(df2)
if isStationary :
    # Execution of arma
    print("Execution of arma")
else :
    # Transmormation to stationary
    print("Transformation to stationary")
