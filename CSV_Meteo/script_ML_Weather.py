import pandas as pd
from requests import post, get
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv('C:\\Users\\Eros Bignardi\\PycharmProjects\\mergeCSV\\weather_data_notProcessed.csv')

# creazione matrice di features e vettore di label
X = df.drop(columns='animal_class')
y = df['animal_class']

# CREAZIONE TRAIN E TEST CON MODELLO + FIT & PREDICT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# model = KNeighborsClassifier()
model = DecisionTreeClassifier()

model.fit(X_train, y_train)
# predict = model.predict(X_test)

animale = '1377a80b-d0d4-4871-818d-005526c5df01'

url_animale = 'https://ciotolaiot.appspot.com/api/v1/animale/' + animale
r_animale = get(url_animale).json()
print(r_animale)

lat = '44.8804'
lng = '11.0705'
url_weather = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lng + \
              '&exclude=hourly,daily&appid=61fbdbb114aea8d6d7f671413daca2a6'
r_weather = get(url_weather).json()
print(r_weather)

dict = {}
dict['lat'] = r_weather['coord']['lat']
dict['lng'] = r_weather['coord']['lon']
dict['timezone'] = r_weather['timezone']
dict['temp'] = r_weather['main']['temp'] - 273.15
dict['pressure_hpa'] = r_weather['main']['pressure']
dict['humidity_%'] = r_weather['main']['humidity']
dict['clouds'] = r_weather['clouds']['all']
dict['wind_speed'] = r_weather['wind']['speed']
dict['wind_deg'] = r_weather['wind']['deg']
dict['timestamp'] = str(datetime.now())

print(dict)

data_test = pd.DataFrame(dict, index=[0])

columns = data_test.columns
columns = columns.to_list()
print(columns)
to_remove = ['timezone', 'timestamp']
for element in to_remove:
    columns.remove(element)

print(columns)

data_test = data_test.drop(columns=to_remove)
print(data_test)

predict = model.predict(data_test)

print('Class predicted: ' + str(predict))
