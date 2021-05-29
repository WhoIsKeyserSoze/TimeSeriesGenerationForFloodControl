import datetime
import TimeSeriesPredictor as tsp

date = datetime.date(2021, 5, 11)
sensor_code = 'V523401001'

measures_list = tsp.dataGeter.GetMeasures(date, 3, sensor_code)

data = measures_list[:-24]

arma = tsp.arma.PredictFromList(data, 24)
arima = tsp.arima.PredictFromList(data, 24)
sarima = tsp.sarima.PredictFromList(data, 24)
autoarima = tsp.autoarima.PredictFromList(data, 24)
lstm = tsp.LSTM.PredictFromList(data, 24)
bilstm = tsp.BILSTM.PredictFromList(data, 24)
gru = tsp.GRU.PredictFromList(data, 24)

arma.insert(0, data[-1])
arima.insert(0, data[-1])
sarima.insert(0, data[-1])
autoarima.insert(0, data[-1])
lstm.insert(0, data[-1])
bilstm.insert(0, data[-1])
gru.insert(0, data[-1])

tsp.graph.ShowMeasures(measures_list, arma, arima, sarima, autoarima, lstm, bilstm, gru)
