import datetime
import TimeSeriesPredictor as tsp

date = datetime.date(2021, 5, 18)
sensor_code = 'K617313002'

measures_list = tsp.dataGeter.GetMeasures(date, 2, sensor_code)

pre_len = 24
data = measures_list[:-1 * pre_len]

arma = tsp.arma.PredictFromList(data, 24)
arima = tsp.arima.PredictFromList(data, 24)
sarima = tsp.sarima.PredictFromList(data, 24)
autoarima = tsp.autoarima.PredictFromList(data, 24)
lstm = tsp.LSTM.PredictFromList(data, pre_len)
bilstm = tsp.BILSTM.PredictFromList(data, pre_len)
gru = tsp.GRU.PredictFromList(data, pre_len)

arma.insert(0, data[-1])
arima.insert(0, data[-1])
sarima.insert(0, data[-1])
autoarima.insert(0, data[-1])
lstm.insert(0, data[-1])
bilstm.insert(0, data[-1])
gru.insert(0, data[-1])

tsp.graph.ShowMeasures(measures_list, arma, arima, sarima, autoarima)
