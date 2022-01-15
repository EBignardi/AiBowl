from google.cloud import firestore
from requests import post, get
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime
class canile(object):
    def __init__(self):
        self.db=firestore.Client()
        self.posizione='posizione sconosciuta'
        self.tipo='tipo sconosciuto'
        self.num='numero non disponibile'
        self.q='quantità non disponibile'

    def insert_info(self, animale, **kwargs):
        ref=self.db.collection('info').document(f'{animale}')
        try:
            qtc=kwargs.get('quantità_cibo', self.q)
            qtc=qtc/100
            ref.set({
                'animale': animale,
                'numero_pasti': kwargs.get('numero_pasti', self.num),
                'quantità_cibo':qtc,
                'tipo':kwargs.get('tipo', self.tipo)
            })
            return 'ok'
        except:
            return 'not ok'
    def get_info(self, animale):
        try:
            ref=self.db.collection('info').document(f'{animale}')
            ref=ref.get()
            ref=ref.to_dict()
            return ref
        except:
            return None
        
    def get_login(self, username, password):
        try:
            ref=self.db.collection('account').document(f'{username}')
            ref=ref.get()
            ref=ref.to_dict()
            if ref['password']==password:
                return 'ok'
            else:
                return None
        except:
            return None
    
    def get_pos(self, animale):
        lista=[]
        ref=self.db.collection('posizioni')
        for doc in ref.stream():
            diz=doc.to_dict()
            if diz['animale']==animale:
                lista.append(diz)
        return lista
    def getTest(self):
        lista=[]
        ref=self.db.collection('test')
        for doc in ref.stream():
            diz=doc.to_dict()
            lista.append(diz)
        return lista
    def getlist(self):
        lista=[]
        ref=self.db.collection('info')
        for doc in ref.stream():
            diz=doc.to_dict()
            lista.append(diz)
        return lista
    def insert_eat(self, animale, **kwargs):
        docu=animale+str(datetime.now())
        ref=self.db.collection('pasti').document(f'{docu}')
        try:
            long=kwargs.get('long', self.posizione)
            lat=kwargs.get('lat', self.posizione)
            url='https://ciotolaiot.appspot.com/api/v1/info/'+animale
            r=get(url)
            r=r.json()
            tipo=r['tipo']
            quantità=r['quantit\u00e0_cibo']
            url2='https://ciotolaiot.appspot.com/api/v1/ciotola/'+str(lat)+'/'+str(long)
            r1=get(url2)
            r1=r1.json()
            qt=r1['qt']
            if qt>quantità:
                ref.set({
                    'animale': animale,
                    'time': str(datetime.now()),
                    'long': long,
                    'lat': lat                
                })
                cibo=qt-quantità
                r2=post(url2, json={'qt':cibo})
                url1='https://ciotolaiot.appspot.com/api/v1/test/'+str(long)+'/'+str(lat)+'/'+tipo
                print(url1)
                r=post(url1)
            else:
                messaggio='La ciotola alla posizione LAT='+str(lat)+' '+'LONG='+str(long)+' è scarica. Ricaricarla al più presto!'
                url2='https://telegrambotciotolaiot.appspot.com/api/v1/telegram/'+messaggio
                r=get(url2)
                return 'not ok 1'
            return 'ok'
        except:
            return 'not ok'
    def get_mangiato(self, animale):
        lista=[]
        coll=self.db.collection('pasti')
        for doc in coll.stream():
            diz=doc.to_dict()
            if diz['animale']==animale:
                lista.append(diz)
        return lista
        
    def modify_position(self, animale, **kwargs):
        docu=animale+str(datetime.now())
        ref=self.db.collection('posizioni').document(f'{docu}')
        try:
            ref.set({
                'animale': animale,
                'long': kwargs.get('long', self.posizione),
                'lat': kwargs.get('lat', self.posizione),
                'tipo':kwargs.get('tipo', self.tipo),
                'time': str(datetime.now())
            })
            return 'ok'
        except:
            return 'not ok'

    def get_position(self, long,lat, tipo):
        try:
            lista=[]
            coll=self.db.collection('posizioni')
            for doc in coll.stream():
                diz=doc.to_dict()
                if diz['tipo']==tipo and round(diz['long'],3)==round(float(long),3) and round(diz['lat'],3)==round(float(lat),3):
                    lista.append(diz)
            if len(lista)>0:
                dict={}
                dict=lista[-1]
                url='https://ciotolaiot.appspot.com/api/v1/mangiato/'+dict['animale']
                url1='https://ciotolaiot.appspot.com/api/v1/info/'+dict['animale']
                r=get(url)
                r1=get(url1)
                r1=r1.json()
                if r.status_code==400:
                    return r1
                else:
                    r=r.json()

                    ultimo=r[-1]
                    ora=ultimo['time'].split('.')
                    date_time_obj = datetime.strptime(ora[0], '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - date_time_obj).total_seconds() / 60.0 >= (1440/int(r1['numero_pasti'])):
                        return r1
                        #fai la post nel bridge    
                    else:
                        return None
            else:
                return None
        except :
            return None
    

    def insert_df(self, long, lat,tipo):
        url='https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(long)+'&exclude=hourly,daily&appid=61fbdbb114aea8d6d7f671413daca2a6'
        r=get(url)
        r=r.json()
        dict={}
        ref=self.db.collection('test').document(f'{str(datetime.now())}')
        try:
            ref.set({
                'lat':r['coord']['lat'],
                'lng':r['coord']['lon'],
                'timezone':r['timezone'],
                'temp':r['main']['temp']-273.15,
                'pressure_hpa':r['main']['pressure'],
                'humidity_%':r['main']['humidity'],
                'clouds':r['clouds']['all'],
                'wind_speed':r['wind']['speed'],
                'wind_deg':r['wind']['deg'],
                'tipo':tipo,
                'timestamp':str(datetime.now())
            })
        except:
            return 'not ok'
        return 'ok'
    def insert_info_ciot(self, lat, lng,**kwargs):
        id=str(lat)+' '+str(lng)
        ref=self.db.collection('ciotola').document(f'{id}')
        try:
            ref.set({
                'lat':lat,
                'lng':lng,
                'qt':kwargs.get('qt', self.q)
            })
        except:
            return 'not ok'
        return 'ok'
    def getCiotola(self, lat, lng):
        try:
            id=str(lat)+' '+str(lng)
            ref=self.db.collection('ciotola').document(f'{id}')
            ref=ref.get()
            ref=ref.to_dict()
            return ref
        except:
            return None
        
    def getClass(self, lat, lng):
        url='https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lng)+'&exclude=hourly,daily&appid=61fbdbb114aea8d6d7f671413daca2a6'
        r=get(url)
        r=r.json()
        dict={}
        dict['lat']=r['coord']['lat']
        dict['lng']=r['coord']['lon']
        dict['timezone']=r['timezone']
        dict['temp']=r['main']['temp']-273.15
        dict['pressure_hpa']=r['main']['pressure']
        dict['humidity_%']=r['main']['humidity']
        dict['clouds']=r['clouds']['all']
        dict['wind_speed']=r['wind']['speed']
        dict['wind_deg']=r['wind']['deg']
        
        data_test = pd.DataFrame(dict, index=[0])
        r1=get('https://ciotolaiot.appspot.com/api/v1/dftest')
        r1=r1.json()
        print(r1)
        for x in r1:
            x.pop('timestamp')
        data_train=pd.DataFrame(r1)
        X = data_train.drop(columns='tipo')
        y = data_train['tipo']
        model = DecisionTreeClassifier()
        model.fit(X, y)
        predict = model.predict(data_test)
        model.fit(X, y)
        predict1 = model.predict(data_test)
        model.fit(X, y)
        predict2 = model.predict(data_test)

        dict={}
        dict['tipo1']=predict[0]

        dict['tipo2']=predict1[0]

        dict['tipo3']=predict2[0]

        

        return dict