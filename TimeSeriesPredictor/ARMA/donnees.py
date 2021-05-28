import urllib.request
import datetime

# Base url to build observations request
base_obs_url = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr?"
# Differents constants for request
sensor_code_format = "code_entite="
start_date_format = "date_debut_obs="
end_date_format = "date_fin_obs="
measures_type_format = "grandeur_hydro="
nb_obs_format = "size="
nb_obs = 4096

# returns the list of measures took since the start_date 'date' during the 'duration' (in days) from the 'sensor'
# it will return [] if an error occured (bad date entry or failure to connect to the hubeau's API)
def get_measures(start_date, duration, sensor_code, measure_type) :

    # Checks if all arguments are valids
    end_date = start_date + datetime.timedelta(days = duration)
    if(not (are_dates_in_range(start_date, end_date) and is_sensor_code_valide(sensor_code))):
        return []

    # Builds URL
    URL = base_obs_url

    URL += (sensor_code_format + str(sensor_code) + '&')
    URL += (start_date_format + start_date.strftime("%Y-%m-%d") + '&')
    URL += (end_date_format + end_date.strftime("%Y-%m-%d") + '&')
    URL += (nb_obs_format + str(nb_obs) + '&')
    URL += (measures_type_format + measure_type)

    # Get string contening all infos
    infos = get_data(URL)
    if(infos == "") :
        return []

    # Gather measures from string
    measures = extract_measures(infos)

    # return all measures
    return measures

# Gets the page code from the given URL
def get_data(URL) :
    # open a connection to a URL
    webUrl=urllib.request.urlopen(URL)
    # Check return code from the Hubeau API if there is no issue
    return_code=str(webUrl.getcode())
    if(return_code != "200" and return_code != "206") :
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

# returns if both dates are within 30 days from today and not in the future
def are_dates_in_range(start_date, end_date) :
    diff_start = (datetime.date.today() - start_date)
    diff_end = (datetime.date.today() - end_date)
    return diff_start.days >= 0 and diff_start.days < 31 and diff_end.days >= 0 and diff_end.days < 31

# checks if the sensor exists
def is_sensor_code_valide(sensor_code) :
    # TODO ?
    return True
