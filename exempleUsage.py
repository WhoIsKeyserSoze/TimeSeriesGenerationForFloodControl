import donnees
import datetime
import graph
import pandas
import random

today = datetime.date.today()
duration = 3
height = 'H'
flow = 'Q'

sensor_list = ['O004402001', 'Y523501001',
               'Q732252001', 'P608151001', 'L421071001', 'K447001001', 'I311301001', 'H517311001', 'U060001001', 'V415401001']


while(True) :
    # get random sensor
    sensor_code = sensor_list[random.randrange(0,len(sensor_list)-1,1)]

    # gen random date
    off_set = random.randrange(1,29,1)
    if(today.day > off_set) :
        start_date = datetime.date(today.year, today.month, today.day - off_set)
    else : 
        start_date = datetime.date(today.year, today.month-1, 31 - (off_set - today.day))

    #get measures
    height_measures = donnees.get_measures(start_date, duration, sensor_code, height)
    height_lst, date_lst = zip(*height_measures)

    # export to csv
    height_lst = list(height_lst)
    date_lst = list(date_lst)
    df =  pandas.DataFrame({'date': date_lst, 'height' : height_lst})
    filename = str(start_date) + '_' + sensor_code
    df.to_csv(r'D:Desktop\Prog\L3\BE\SomeData\\' +filename+ '.csv', index=False)