import datetime
import dataGeter
import graph
import process_pred

date = datetime.date(2021, 5, 15)
sensor_code = 'K268081001'


measures_list = dataGeter.GetMeasures(date, 10, sensor_code)
prediction = []
prediction = process.predict_arma(measures_list[:72],24)

graph.ShowMeasures(measures_list, prediction)
