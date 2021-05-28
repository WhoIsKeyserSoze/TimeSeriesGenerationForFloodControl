import datetime

import dataGeter
import graph

from LSTM_module import LSTM


date = datetime.date(2021, 5, 20)
duration = 4
value_type = 'H'
sensor_code = 'K236301001'

measures = dataGeter.get_measures(date, duration, sensor_code)
pred = LSTM.PredictFromList(measures[24:48], 24)

graph.show_measures(measures, measures[24:48], pred)
