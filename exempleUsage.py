import donnees
import datetime
import graph

start_date = datetime.date(2021, 4, 7)
duration = 1
sensor_code = "O004402001"
height = 'H'
flow = 'Q'

height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
flow_measures = donnees.get_measures(start_date, duration, sensor_code, flow)

graph.show_measures(height_measures, flow_measures)
