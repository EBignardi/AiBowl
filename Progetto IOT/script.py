import geocoder
import time
from requests import post, get
from datetime import datetime
class WeatherInfo():
        
    def setup(self):
        g = geocoder.ip('me')
        self.lat=g.latlng[0]
        self.lng=g.latlng[1]
    def loop(self):
        
        while (True):
            url='api.openweathermap.org/data/2.5/weather?lat='+self.lat+'&lon='+self.lng+'&appid=61fbdbb114aea8d6d7f671413daca2a6'
            r=get(url)
            r=r.json()
            dict={}
            dict['lat']=r['lat']
            dict['lng']=r['lon']
            dict['timezone']=r['timezone']
            dict['temp']=r['current']['temp']-273.15
            dict['pressure_hpa']=r['current']['pressure']
            dict['humidity_%']=r['current']['humidity']
            dict['clouds']=r['current']['clouds']
            dict['wind_speed']=r['current']['wind_speed']
            dict['wind_deg']=r['current']['wind_deg']
            name='sample'+datetime.now()+'.csv'
            a_file = open(name, "w")
            writer = csv.writer(a_file)
            for key, value in dict.items():
                writer.writerow([key, value])
            a_file.close()


if __name__ == '__main__':
    br=WeatherInfo()
    br.loop()