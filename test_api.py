import datetime

import TimeSeriesPredictor as tsp

date = datetime.date(2021, 5, 19)
sensor_code = 'O711502001'

measures_list = tsp.dataGeter.GetMeasures(date, 3, sensor_code)

prediction = []
data = measures_list[:-24]
prediction = tsp.LSTM.PredictFromList(measures_list[:-24], 24)

prediction.insert(0, data[-1])

tsp.graph.ShowMeasures(measures_list, prediction)
