import donnees
import datetime
import graph
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

start_date = datetime.date(2021, 4, 7)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'

height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
flow_measures = donnees.get_measures(start_date, duration, sensor_code, flow)

#graph.show_measures(height_measures, flow_measures)

# Puts the data into a pandas DataFrame
df = pd.DataFrame(height_measures, columns = ['date','height'])
df['date'] = pd.to_datetime(df.date)
df.set_index('date', inplace=True)
print(df.head())

# plots the acf
acf_plot = plot_acf(df.height, lags=96)
plt.show()

pacf_plot = plot_pacf(df.height)
plt.show()
