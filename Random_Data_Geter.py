import donnees
import datetime
import graph
import pandas
import random

today = datetime.date.today()
duration = 3 #days
height = 'H'
flow = 'Q'

unclassified_path = r'D:Desktop\Prog\L3\BE\SomeData'

sensor_list = ['O004402001', 'Y523501001',
               'Q732252001', 'P608151001', 
               'L421071001', 'K447001001', 
               'I311301001', 'H517311001', 
               'U060001001', 'V415401001',
               'H220101001', 'A341020001',
               'A261020001', 'B222001001',
               'A433301001', 'V453001002',
               'V720000501', 'O256292001',]

i = 0
while(i <= 60) :
    
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
    if(len(height_measures) > 2):
        i += 1
        date_lst, height_lst = zip(*height_measures)

        # export to csv
        height_lst = list(height_lst)
        date_lst = list(date_lst)
        df =  pandas.DataFrame({'date': date_lst[::-1], 'height' : height_lst[::-1]})
        filename = str(start_date) + '_' + sensor_code
        df.to_csv(unclassified_path + '\\' +filename+ '.csv', index=False)
