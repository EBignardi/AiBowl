import csv
from requests import post, get
import pandas as pd


def import_csv(csvfilename):
    row_index = 0
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if row:  # avoid blank lines
                row_index += 1
                columns = [str(row_index)]
                data.append(columns)
    return data


# insert new value in csv file, after each animal eat (to save weather condition)
# list of column names
data = import_csv('C:\\Users\\Eros Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed.csv')
last_row_index = data[-1][0]
last_row_index_new = str(int(int(last_row_index) - 1))
print(last_row_index_new)

df = pd.read_csv('C:\\Users\\Eros Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed.csv')

field_names = ['id', 'lat', 'lng', 'temp', 'pressure_hpa', 'humidity_%', 'clouds', 'wind_speed', 'wind_deg',
               'animal_class']

# Dictionary
lat = '44.8804'
lng = '11.0705'
animal_class = '3'

url_weather = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lng + \
              '&exclude=hourly,daily&appid=61fbdbb114aea8d6d7f671413daca2a6'

r_weather = get(url_weather).json()
# print(r_weather)

dict_insert = {'id': last_row_index_new,
               'lat': r_weather['coord']['lat'],
               'lng': r_weather['coord']['lon'],
               'temp': r_weather['main']['temp'] - 273.15,
               'pressure_hpa': r_weather['main']['pressure'],
               'humidity_%': r_weather['main']['humidity'],
               'clouds': r_weather['clouds']['all'],
               'wind_speed': r_weather['wind']['speed'],
               'wind_deg': r_weather['wind']['deg'],
               'animal_class': animal_class}  # da modificare in base alla classe dell'animale che ha mangiato
print(dict_insert)

# per rendere il file omogeneo come formattazione with open('C:\\Users\\Eros
# Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed.csv') as in_file: with open('C:\\Users\\Eros
# Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed_out.csv', 'w') as out_file: writer = csv.writer(
# out_file) for row in csv.reader(in_file): if row: writer.writerow(row)

# Open your CSV file in append mode
# Create a file object for this file
with open('C:\\Users\\Eros Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed.csv', 'a') as f_object:
    dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)

    # Pass the dictionary as an argument to the Writerow()
    dictwriter_object.writerow(dict_insert)

    # Close the file object
    f_object.close()


