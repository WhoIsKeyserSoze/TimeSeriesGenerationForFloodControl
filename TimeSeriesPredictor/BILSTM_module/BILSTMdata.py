import dataGeter3 as dataGeter
import datetime
import pandas 
import numpy
import random
import os

# Download and save random data from hubeau's api
def random_data_geter(nb_series, storage_path, period=29) :

    today = datetime.date.today()
    height = 'H'

    sensor_list = dataGeter.GetAllActivesSensors()
    nb_sensors = len(sensor_list)

    i = 0
    while(i <= nb_series) :
        # get random sensor
        sensor_code = sensor_list[random.randrange(0,nb_sensors-1,1)]

        # gen random date
        off_set = random.randrange(1,29,1)
        start_date = datetime.date(today.year, today.month-1, today.day+1)

        #get measures
        height_measures = dataGeter.GetMeasures(
            start_date, period, sensor_code, height)
        if(len(height_measures) > 2):
            i += 1
            print(i)
            date_lst, height_lst = zip(*height_measures)

            # export to csv
            height_lst = list(height_lst)
            date_lst = list(date_lst)
            df =  pandas.DataFrame({'date': date_lst[::-1], 'height' : height_lst[::-1]})
            filename = str(start_date) + '_' + sensor_code
            df.to_csv(storage_path + '\\' +filename+ '.csv', index=False)

# load a file that have been doawnload with the random_data_geter and put it in an array
# only load measure values
# return an array.shape = (theorical_len, 1) 
# it looks like this : array[[measure1], [measure2], [measure3], ...]
def load_file(file_path, file_name, theorical_len):
    df = pandas.read_csv(file_path + '\\' + file_name)
    arr = df.to_numpy()
    final_list = []
    i = 0
    # separate measure and date
    for [date, measure] in arr:
        final_list.append([measure])
        i += 1
    # Because some ST are missing measures and we need all ST to be same length
    # i add the last measure over again until it has 71 measures
    lastmeasure = final_list[-1]
    for j in range(i, theorical_len):
        final_list.append(lastmeasure)

    return numpy.array(final_list)

# load all file in a give directory
# return an array of loaded file
# array.shape = (nb_file, serie_len, 1)
# [st1, st2, st3, ...]
# with st = [[measure1], [measure2], [measure3], ...]
def load_data(files_path, serie_len) :
    data = []
    for file in os.listdir(files_path) :
        if (file.endswith(".csv")) :
            data.append(load_file(files_path, file, serie_len))
    
    return numpy.array(data)

# Return the array with values betwen 0 and 1 and the old max and min value of the array (to un-normalize it)
def normalize_array(arr):
    minValue = numpy.amin(arr)
    maxValue = numpy.amax(arr)
    if(maxValue == minValue) :
        maxValue += 1
    return (arr - minValue) / (maxValue - minValue), minValue, maxValue

# reverse above function
def un_normalize_array(arr, minV, maxV) :
    return (arr * (maxV - minV)) + minV

# return the array of series with all series individualy normalized
# data.shape = (nb_series, nb_measurements, 1)
def normalize_dataset(data) :
    for i in range(len(data)) :
        normalized, minV, maxV = normalize_array(data[i])
        data[i] = normalized
    return data

# make multiple time series from a lager one
# takes seriesList.shape = (nb_series, rawSeriesLen, 1)
# returns [data, targets] with data.shape = (more than nbseries, newSeries_len, 1)
# and targets.shape = (more than nbseries, 1, 1)
def timeSeriesGenerator(seriesList, rawSeriesLen, newSeries_len):
    data = []
    targets = []
    for i in range(len(seriesList)) :
        for j in range( int((rawSeriesLen-1)/newSeries_len) ) :
            newSerie = []
            for k in range(newSeries_len) :
                newSerie.append([seriesList[i][j*24 + k][0]])
            data.append(newSerie)
            targets.append([seriesList[i][24*j + 24]])
        
    return [numpy.array(data), numpy.array(targets)]
