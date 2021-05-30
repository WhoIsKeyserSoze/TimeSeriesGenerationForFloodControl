import datetime
import TimeSeriesPredictor as tsp

date = datetime.date(2021, 5, 10)
sensor_code = 'K480001001'
duration = 2  # jours

# récupères les 2 jours de mesures
measures_list = tsp.dataGeter.GetMeasures(date, duration, sensor_code)
# Sépare ces mesures en deux
data, real = measures_list[:24], measures_list[-25:]
# fait une prédiction à partir de la première partie
pred = tsp.LSTM.PredictFromList(data, 24)
# ajoute en début de la prédiction la dernière mesure du data, afin qu'il n'y ai pas de coupures sur le graph
pred.insert(0, data[-1])
# affiche la première partie, la prédiction et la réalité
tsp.graph.ShowMeasures(data, real, pred)
