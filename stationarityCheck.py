import donnees
import datetime
import graph
import pandas as pd
from math import sqrt

pourcentageErreur = 5
start_date = datetime.date(2021, 4, 11)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'

height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
flow_measures = donnees.get_measures(start_date, duration, sensor_code, flow)

# Puts the data into a pandas DataFrame
df = pd.DataFrame(height_measures, columns = ['date','height'])
df['date'] = pd.to_datetime(df.date)
df.set_index('date', inplace=True)
# print(df.head())

# Check for stationarity with global vs local tests
# 1 : Mean = constant
# 2 : standard deviation = constant
# 3 : No seasonality

split = round(len(df) / 2)
df1, df2 = df[0:split], df[split:]
mean1, mean2 = df1.height.mean(), df2.height.mean()
sd1, sd2 = sqrt(df1.height.var()), sqrt(df2.height.var())
print('mean1 = %f , mean2 = %f ' % (mean1, mean2))
print('standardDeviation1 = %f , standardDeviation2 = %f ' % (sd1, sd2))
err = pourcentageErreur*(mean1+mean2)/200
print("Erreur acceptable : ", err)
if (abs(mean1-mean2))>err :
    print("La serie n'est pas stationnaire")
else :
    print("La serie est stationnaire")
