import datetime

import dataGeter
import graph

from LSTM_module import LSTM


date = datetime.date(2021, 5, 25)
duration = 2
sensor_code = 'K236301001'

measures = dataGeter.GetLastMeasures(sensor_code)
pred = LSTM.PredictFromSensor(sensor_code, 24)

pred.insert(0, measures[-1])

graph.ShowMeasures(measures, pred)
