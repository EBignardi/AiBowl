from flask import Flask, request, render_template
from wtforms import Form, StringField, SubmitField, validators
from uuid import UUID
from config import Config
from flask import  jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk

import googlemaps
import pandas as pd
from geopy import distance
from requests import post, get
app = Flask(__name__)
myconfig = Config
app.config.from_object(myconfig)
db = SQLAlchemy(app)


gmaps = googlemaps.Client(key=Config.GOOGLEMAPS_APIKEY)


class Sensorfeed(db.Model):
    id = db.Column('feed_id', db.Integer, primary_key = True)
    description = db.Column('description', db.String)
    value = db.Column('value', db.Integer)
    lat = db.Column('lat', db.Integer)
    long = db.Column('long', db.Integer)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow)
    def __init__(self, description, value, lat, long):
        self.value = value
        self.lat = lat
        self.long = long
        self.description = description

def distanceLatLong(p0, p1, p2): # p0 is the point
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    d2 = dx*dx + dy*dy

    nx = ((x0-x1)*dx + (y0-y1)*dy) / d2
    if nx >= 0 and nx <= 1:
        nearest = (dx*nx + x1, dy*nx + y1)
        result = distance.distance(p0, nearest).km
    else:
        if distance.distance(p0, p1)<distance.distance(p0,p2):
            nearest = p1
            result = distance.distance(p0, p1).km
        else:
            nearest = p2
            result = distance.distance(p0, p2).km

    return result, nearest




class InsertForm(Form):
    animale = StringField('Animal')
    tipo=StringField('Tipo')
    numero_pasti = StringField('Numero pasti')
    quantità_cibo=StringField('Quantità cibo')
    submit = SubmitField(label=('Submit'))
class InsertFood(Form):
    lat = StringField('Lat')
    lng=StringField('Long')
    quantità_cibo_aggiunta=StringField('Quantità cibo aggiunta')
    submit = SubmitField(label=('Submit'))

class LogForm(Form):
    username=StringField('Username')
    password=StringField('password')
    submit = SubmitField(label=('Submit'))
class LatLngForm(Form):
    lat=StringField(('Latitudine'))
    lng=StringField(('Longitudine'))
    submit = SubmitField(label=('Submit'))

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj=UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test
def validatenumber(num):
    try:
        if int(num):
            return num
    except:
        return False
def validate_qt(qt):
    try:
        if int(qt):
            return qt
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')
@app.route('/test', methods=['GET', 'POST'])
def test():
    form=LatLngForm()
    if request.method=='GET':
        return render_template('test.html', form=form )
    else:
        lat=request.form['lat']
        print('questa è lat')
        print(lat)
        print('ecco')
        lng=request.form['lng']
        print('questa è lng')
        print(lat)
        print('ecco')
        url='http://127.0.0.1:5000/api/v1/ml/'+str(lat)+'/'+str(lng)
        r=get(url)
        r=r.json()
        print(r)
        #3 predizioni
        listan=[]
        cont=0
        diz={}
        i=1
        
        while i<=len(r):
            if r['tipo'+str(i)] not in listan:
                listan.append(r['tipo'+str(i)])
                j=1
                while j<=len(r):
                    if r['tipo'+str(j)]== r['tipo'+str(i)]:
                        cont=cont+1
                    j=j+1
                diz[r['tipo'+str(i)]]=100/3*cont
                cont=0
            i=i+1
        print(diz)
        return render_template('test.html', form=form, diz=diz )

@app.route('/insert', methods=['GET','POST'])
def insert():
    form=LogForm()
    if request.method=='GET':
        return render_template('login.html', form=form, status='first')
    else:
        username=request.form['username']
        password=request.form['password']
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('login.html', form=form, status='no')
        else:
            return render_template('login.html', form=form, status='yes', username=username, password=password)
@app.route('/update', methods=['GET','POST'])
def update():
    form=LogForm()
    if request.method=='GET':
        return render_template('login2.html', form=form, status='first')
    else:
        username=request.form['username']
        password=request.form['password']
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('login2.html', form=form, status='no')
        else:
            return render_template('login2.html', form=form, status='yes', username=username, password=password)
@app.route('/list', methods=['GET'])
def list():
    try:    
        db.drop_all()
        db.create_all()
        
        r2=get('https://ciotolaiot.appspot.com/api/v1/list')
        r2=r2.json()
        for x in r2: 
            url='https://ciotolaiot.appspot.com/api/v1/animale/'+x['animale']
            r=get(url)
            r=r.json()
            r1=[]
            try:
                for x in r:
                    if int(x['lat'])!=0 and int (x['long'])!=0:
                        r1.append(x)
                ultimo=r1[-1]
                sampleval=Sensorfeed(description=ultimo['animale'], value=str(ultimo['time'])+' '+str(ultimo['tipo']), lat=ultimo['lat'], long=ultimo['long'])
                db.session.add(sampleval)
            except:
                print("nessuna info disponibile sull' animale: "+ x['animale'])    
        db.session.commit()
        elenco=Sensorfeed.query.all()
        for curpoint in elenco:
            #check if val is in polyline
            print(curpoint.lat)
            print(curpoint.long)
        return render_template('mappa.html', lista=elenco, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myMap')

    except:
        return render_template('error.html')
@app.route('/animal/<string:animale>', methods=['GET'])
def animal(animale):
    try:
        now = datetime.now()
        db.drop_all()
        db.create_all()
        url='https://ciotolaiot.appspot.com/api/v1/animale/'+animale
        r=get(url)
        r=r.json()
        r1=[]
        for x in r:
            if int(x['lat'])!=0 and int (x['long'])!=0:
                r1.append(x)
        primo=r1[0]
        ultimo=r1[-1]
        primo=r1[0]
        routefrom=((str(primo['lat'])+', '+str(primo['long'])))
        routeto=(str(ultimo['lat'])+', '+str(ultimo['long']))
        latlng=[]
        dict={}
        directions_result = gmaps.directions(routefrom,routeto,
                                             mode="transit",
                                             departure_time=now)
        bestdirection=directions_result[0]
        polyline_encoded=bestdirection['overview_polyline']
        polyline_decoded = googlemaps.convert.decode_polyline(polyline_encoded['points'])
        for x in r1:
            dict['lat']=x['lat']
            dict['lng']=x['long']
            sampleval=Sensorfeed(description=animale, value=x['time'], lat=x['lat'], long=x['long'])
            db.session.add(sampleval)
            latlng.append(dict)
            dict={}
        db.session.commit()
        elenco=Sensorfeed.query.all()
        mioelenco=[]
        elenconearest=[]
        for curpoint in elenco:
            #check if val is in polyline
            pointpos = (curpoint.lat, curpoint.long)
            mindist=-1
            nearestpp=None

            for i in range(len(polyline_decoded)-1):
                dist, nearestpoint = distanceLatLong(pointpos,
                                (polyline_decoded[i]['lat'],polyline_decoded[i]['lng']),
                                (polyline_decoded[i+1]['lat'],polyline_decoded[i+1]['lng'])
                                )
                if mindist==-1 or mindist>dist:
                    mindist=dist
                    nearestpp=nearestpoint
            if mindist<Config.DISTTH:
                mioelenco.append(curpoint)
                elenconearest.append(nearestpp)
        polyline_decoded = str(polyline_decoded).replace('"','').replace("'",'')
        mioelencojs = "["
        for val in mioelenco:
            elem = "title: '{title}',description:'{descr}', lat:{lat},lng:{lng}".format(
                title=val.description, descr=val.value, lat=val.lat, lng=val.long)
            mioelencojs=mioelencojs+"{"+elem+"}"
        mioelencojson=mioelencojs+"]"
        elem='[{'+elem+'}]'
        #return render_template('mappa2.html', param=polyline_decoded, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myRoute')
        return render_template('mappa2.html', param={'points':elem, 'nearest':[], 'route':polyline_decoded}, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myPointOnaRoute')

    except:
        return render_template('error.html') 
        
@app.route('/points')
def points():
    elenco=Sensorfeed.query.all()
    mioelenco=[]
    for val in elenco:
        elem = {
            'title': val.description,
            'description' : str(val.value),
            'lat' : val.lat,
            'lng' : val.long
        }
        mioelenco.append(elem)
    outval = {'listaPunti': mioelenco}

    return jsonify(outval)

@app.route ('/route')
def getroute():
    now = datetime.now()
    routefrom="Disneyland"
    routeto ="Universal Studios Hollywood"
    routefrom='44.63757242419685, 10.94673393566677'
    routeto = '44.62306550033823, 10.98149536630288'
    directions_result = gmaps.directions(routefrom,routeto,
                                     mode="transit",
                                     departure_time=now)

    bestdirection=directions_result[0]
    polyline_encoded=bestdirection['overview_polyline']
    polyline_decoded = googlemaps.convert.decode_polyline(polyline_encoded['points'])
    polyline_decoded = str(polyline_decoded).replace('"','').replace("'",'')
    return render_template('mappa.html', param=polyline_decoded, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myRoute')

@app.route ('/points_onaroute')
def pointsonaroute():
    now = datetime.now()
    routefrom="Disneyland"
    routeto ="Universal Studios Hollywood"
    routefrom='44.63757242419685, 10.94673393566677'
    routeto = '44.62306550033823, 10.98149536630288'

    directions_result = gmaps.directions(routefrom,routeto,
                                         mode="transit",
                                         departure_time=now)

    bestdirection=directions_result[0]
    polyline_encoded=bestdirection['overview_polyline']
    polyline_decoded = googlemaps.convert.decode_polyline(polyline_encoded['points'])


    elenco=Sensorfeed.query.all()
    mioelenco=[]
    elenconearest=[]
    for curpoint in elenco:
        #check if val is in polyline
        pointpos = (curpoint.lat, curpoint.long)
        mindist=-1
        nearestpp=None

        for i in range(len(polyline_decoded)-1):
            dist, nearestpoint = distanceLatLong(pointpos,
                            (polyline_decoded[i]['lat'],polyline_decoded[i]['lng']),
                            (polyline_decoded[i+1]['lat'],polyline_decoded[i+1]['lng'])
                            )
            if mindist==-1 or mindist>dist:
                mindist=dist
                nearestpp=nearestpoint
        if mindist<Config.DISTTH:
            mioelenco.append(curpoint)
            elenconearest.append(nearestpp)
    polyline_decoded = str(polyline_decoded).replace('"','').replace("'",'')
    mioelencojs = "["
    for val in mioelenco:
        elem = "title: '{title}',description:'{descr}', lat:{lat},lng:{lng}".format(
            title=val.description, descr=val.value, lat=val.lat, lng=val.long)
        mioelencojs=mioelencojs+"{"+elem+"}"
    mioelencojson=mioelencojs+"]"
    print(mioelencojson)
    print(elenconearest)
    print(polyline_decoded)
    return render_template('mappa.html', param={'points':mioelencojson, 'nearest':elenconearest, 'route':polyline_decoded}, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myPointOnaRoute')




@app.route('/admininsert/<string:username>/<string:password>', methods=['GET', 'POST'])
def insert_animal(username, password):
    form = InsertForm()
    if request.method=='GET':
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('error.html')
        return render_template('insert_uuid.html', form=form)
    else:
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('error.html')

        try:
            animale  = request.form['animale']
            numero_pasti = request.form['numero_pasti']
            quantità_cibo=request.form['quantità_cibo']
            tipo=request.form['tipo']
        except:
            animale="animale a caso"
            numero_pasti="animale a caso"
            quantità_cibo='quantità a caso'
        if not validate_uuid(animale):
            return render_template('insert_uuid.html', form=form, error=f"Inserisci il nuovo animale", username=username, password=password)
        if not validatenumber(numero_pasti):
            return render_template('insert_uuid.html', form=form, error=f"Inserisci il nuovo animale", username=username, password=password)
        url='https://ciotolaiot.appspot.com/api/v1/info/'+animale
        num=int(numero_pasti)
        qta=int(quantità_cibo)
        r=post(url, json={'numero_pasti': num, 'quantità_cibo':qta, 'tipo':tipo})
        if r.status_code==201:
            return render_template('insert_uuid.html', form=form, response="Value inserted correctly", username=username, password=password)
        else:
            return render_template('insert_uuid.html', form=form, error=f"Inserisci il nuovo animale", username=username, password=password)
@app.route('/adminupdateciotola/<string:username>/<string:password>', methods=['GET', 'POST'])
def insert_food(username, password):
    form = InsertFood()
    if request.method=='GET':
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('error.html')
        return render_template('insert_uuid.html', form=form)
    else:
        url='https://ciotolaiot.appspot.com/api/v1/login/'+username+'/'+password
        r=get(url)
        if r.status_code!=200:
            return render_template('error.html')

        try:
            lat  = request.form['lat']
            lng = request.form['lng']
            quantità_cibo_aggiunta=request.form['quantità_cibo_aggiunta']
            
        except:
            lat="lat a caso"
            lng="lng a caso"
            quantità_cibo_aggiunta='quantità a caso'
        if not validate_qt(quantità_cibo_aggiunta):
            return render_template('insert_qt.html', form=form, error=f"Inserisci la quantità aggiunta", username=username, password=password)
        url1='https://ciotolaiot.appspot.com/api/v1/ciotola/'+str(lat)+'/'+str(lng)
        r=get(url1)
        r=r.json()
        qt=r['qt']
        url='https://ciotolaiot.appspot.com/api/v1/ciotola/'+str(lat)+'/'+str(lng)
        
        qta=int(quantità_cibo_aggiunta)+int(qt)
        r=post(url, json={'qt':qta})
        if r.status_code==201:
            return render_template('insert_qt.html', form=form, response="Value inserted correctly", username=username, password=password)
        else:
            return render_template('insert_qt.html', form=form, error=f"Inserisci il nuovo animale", username=username, password=password)   

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)