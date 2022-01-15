import geocoder
import csv
import time
from requests import post, get
from datetime import datetime
class WeatherInfo():
        
    def setup(self):
        g = geocoder.ip('me')
        self.lat=g.latlng[0]
        self.lng=g.latlng[1]
    def loop(self):
        i=0
        while (True):
            i=i+1
            url='https://api.openweathermap.org/data/2.5/weather?lat='+str(self.lat)+'&lon='+str(self.lng)+'&exclude=hourly,daily&appid=61fbdbb114aea8d6d7f671413daca2a6'
            print(url)
            r=get(url)
            r=r.json()
            dict={}
            print(r)
            dict['lat']=r['coord']['lat']
            dict['lng']=r['coord']['lon']
            dict['timezone']=r['timezone']
            dict['temp']=r['main']['temp']-273.15
            dict['pressure_hpa']=r['main']['pressure']
            dict['humidity_%']=r['main']['humidity']
            dict['clouds']=r['clouds']['all']
            dict['wind_speed']=r['wind']['speed']
            dict['wind_deg']=r['wind']['deg']
            dict['timestamp']=datetime.now()
            name='sample'+str(i)+'.csv'
            a_file = open(name, "w")
            writer = csv.writer(a_file)
            for key, value in dict.items():
                writer.writerow([key, value])
            a_file.close()
            time.sleep(60)


if __name__ == '__main__':
    br=WeatherInfo()
    br.setup()
    br.loop()