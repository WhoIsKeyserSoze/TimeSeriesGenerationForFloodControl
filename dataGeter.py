import urllib.request
import datetime

# Base url to build observations request
base_obs_url = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr?"
# Differents constants for request
sensor_code_format = "code_entite="
start_date_format = "date_debut_obs="
end_date_format = "date_fin_obs="
time_step_format = "timestep="
measures_type_format = "grandeur_hydro="
nb_obs_format = "size="
nb_obs = 4096

def takeDate(measure) :
    return measure[0]

# returns the list of measures took since the start_date 'date' during the 'duration' (in days) from the 'sensor'
# it will return [] if an error occured (bad date entry or failure to connect to the hubeau's API)
# (datetime.datetime, int, str, str)
def GetMeasures(start_date, duration, sensor_code, measure_type = 'H', time_step = 60) :

    # Checks if all arguments are valids
    end_date = start_date + datetime.timedelta(days = duration)
    if(not (are_dates_in_range(start_date, end_date))):
        return []

    # Builds URL
    URL = base_obs_url

    URL += (sensor_code_format + str(sensor_code) + '&')
    URL += (start_date_format + start_date.strftime("%Y-%m-%d") + '&')
    URL += (end_date_format + end_date.strftime("%Y-%m-%d") + '&')
    URL += (nb_obs_format + str(nb_obs) + '&')
    URL += (time_step_format + str(time_step) + '&')
    URL += (measures_type_format + measure_type)

    # Get string contening all infos
    infos = get_data(URL)
    if(infos == "") :
        return []

    # Gather measures from string
    measures = extract_measures(infos)
    measures.sort(key=takeDate)
    # try to interpolate the value of potential missing measurements
    measures = interpolate(measures, time_step)

    return measures

# return a list contening 24 last measures (one per hour)
# starting 4 hours from now
# If today at 10AM i do a request i'll get 24 measures from yesterday 6AM to today 6AM
def GetLastMeasures(sensor_code) :
    # It is necessary because it seems that sensor's measure take few hours to get on the hubeau's API
    hour_offset = 4
    start_date = datetime.datetime.now() - datetime.timedelta(days=1, hours=hour_offset)
    end_date = datetime.datetime.now() - datetime.timedelta(days=0, hours=hour_offset)

    # Builds URL
    URL = base_obs_url

    URL += (sensor_code_format + str(sensor_code) + '&')
    URL += (start_date_format + start_date.strftime("%Y-%m-%dT%H:00:00") + '&')
    URL += (end_date_format + end_date.strftime("%Y-%m-%dT%H:00:00") + '&')
    URL += (nb_obs_format + str(24) + '&')
    URL += (time_step_format + str(60) + '&')
    URL += (measures_type_format + 'H')

    # Get string contening all infos
    infos = get_data(URL)
    if(infos == ""):
        return []

    # Gather measures from string
    measures = extract_measures(infos)
    measures.sort(key=takeDate)
    # try to interpolate the value of potential missing measurements
    measures = interpolate(measures, 60);

    return measures

# Gets the page code from the given URL
def get_data(URL) :
    # open a connection to a URL
    webUrl=urllib.request.urlopen(URL)
    # Check return code from the Hubeau API if there is no issue
    return_code=str(webUrl.getcode())
    if(return_code != "200" and return_code != "206") :
        # mettre un warning
        return ""
    # Gather all the info requested
    data=webUrl.read()

    return return_code + str(data)

# identifies and returns all measure from the infos string
def extract_measures(infos) :
    resultats = []

    # For each measure
    cursor = infos.find('"date_obs"')
    while(cursor >= 0) :
        # get the measure's date
        date = datetime.datetime.strptime(
            infos[cursor+12:cursor+31], "%Y-%m-%dT%H:%M:%S")
        
        # get the measure
        end_cursor = infos[cursor+49:].find(',')
        measure = float(infos[cursor+49:cursor+49+end_cursor])

        # add them to the list 
        resultats.append((date, measure))

        # remove all treated infos and look for next measure
        infos = infos[cursor+17:]
        cursor = infos.find('"date_obs"')

    return resultats

# return all sensor's code within the hubeau's api response from GetAllActivesSensors() request
def extract_sensor(infos) :
    resultats = []

    # For each measure
    cursor = infos.find('"code_station"')
    while(cursor >= 0) :  
        # get the sensor's code
        sensor = infos[cursor+16:cursor+26]

        # add them to the list 
        resultats.append(sensor)

        # remove all treated infos and look for next measure
        infos = infos[cursor+17:]
        cursor = infos.find('"code_station"')

    return resultats

# returns if both dates are within 30 days from today and not in the future
def are_dates_in_range(start_date, end_date) :
    diff_start = (datetime.date.today() - start_date)
    diff_end = (datetime.date.today() - end_date)
    return diff_start.days >= 0 and diff_start.days < 31 and diff_end.days >= 0 and diff_end.days < 31

# returns a list contening all active sensor's code in france
def GetAllActivesSensors():
    
    region_code = [84, 27, 53, 24, 94, 44, 32, 11, 28, 75, 76, 52, 93]

    sensor_code_list = []

    # Builds URL
    for code in region_code :
        URL = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/referentiel/stations?code_departement=&code_region="+ str(84) +"&en_service=true&format=json"
        rawData = get_data(URL)

        sensor_code_list += extract_sensor(rawData)

    
    return sensor_code_list

# try to interpolate the value of potential missing measurements
# using linear interpolation
def interpolate(measures, timeStep) :

    time = measures[0][0]
    delta = datetime.timedelta(minutes=timeStep)
    prevValue = measures[0][1]
    i = 1
    while(i < len(measures)):
        theoricalTime = time + delta
        if(theoricalTime < measures[i][0]) :
            interValue = (prevValue + measures[i][1]) / 2
            measures.insert(i, (theoricalTime, interValue))
            i -= 1
        prevValue = measures[i][1]
        time = measures[i][0]
        i += 1
    
    return measures
