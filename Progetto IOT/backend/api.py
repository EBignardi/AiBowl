from flask import Flask, request
from flask_restful import Resource, Api
from canile import canile
from uuid import UUID
from datetime import datetime
app=Flask(__name__)
api=Api(app)
basePath='/api/v1'
canile=canile()

def validate_body(json):
    if 'posizione' not in json and 'tipo' not in json:
        return False
    else :
        return json

def validate_body2(json):
    if 'numero_pasti' not in json and 'quantità_cibo' not in json and 'tipo' not in json:
        return False
    else :
        return json


def validate_body3(json):
    if 'long' not in json and 'lat' not in json:
        return False
    else :
        return json
def validate_bodyciot(json):
    if 'qt' not in json:
        return False
    else:
        return json

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj=UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test

class login(Resource):
    def get(self, username, password):
        return_value=canile.get_login(username, password)
        if return_value == 'ok':
            return return_value, 200
        else: 
            return None, 400
#api che permette all'animale di condividere la propria posizione
class animal(Resource):
    def get(self, animale):
        return_value=canile.get_pos(animale)
        if return_value:
            return return_value, 200
        else: 
            return None, 400
        
    def post(self, animale):
        if not validate_uuid(animale):
            return None, 400
        if not request.is_json: 
            return None, 400
        json=request.get_json()
        body=validate_body(json)

        if not body:
            return None, 400
        
        return_value=canile.modify_position(animale,**body)

        if return_value=='ok':
            return None, 201
        else: 
            return None, 400

class posizione(Resource):
    def get(self, long,lat, tipo):
        return_value=canile.get_position(long,lat, tipo)
        if return_value:
            return return_value, 200
        else: 
            return None, 400
class mangiato(Resource):
    def get(self, animale):
        return_value=canile.get_mangiato(animale)
        if return_value:
            return return_value, 200
        else:
            return None, 400
    def post(self, animale):
        if not validate_uuid(animale):
            return None, 401
        if not request.is_json: 
            return None, 402
        json=request.get_json()
        body=validate_body3(json)

        
        return_value=canile.insert_eat(animale, **body)

        if return_value=='ok':
            return None, 201
        elif return_value=='not ok 1': 
            return None, 403
        else:
            return None, 404
class info(Resource):
    def get(self, animale):
        return_value=canile.get_info(animale)
        if return_value:
            return return_value, 200
        else:
            return None, 400
    def post(self, animale):
        if not validate_uuid(animale):
            return None, 400
        if not request.is_json: 
            return None, 400
        json=request.get_json()
        body=validate_body2(json)

        if not body:
            return None, 400
        
        return_value=canile.insert_info(animale,**body)

        if return_value=='ok':
            return None, 201
        else: 
            return None, 404
class list(Resource):
    def get(self):
        return_value=canile.getlist()
        if return_value:
            return return_value, 200
        else:
            return None, 400

class test(Resource):
    def post(self, long, lat, tipo):
        return_value=canile.insert_df(long, lat,tipo)
        if return_value:
            return return_value, 200
        else:
            return None, 400
class dftest(Resource):
    def get(self):
        return_value=canile.getTest()
        if return_value:
            return return_value, 200
        else:
            return None, 400
class ml(Resource):
    def get(self, lat, lng):
        return_value=canile.getClass(lat, lng)
        if return_value:
            return return_value, 200
        else:
            return None, 400
class ciotola(Resource):
    def get(self, lat, lng):
        return_value=canile.getCiotola(lat, lng)
        if return_value:
            return return_value, 200
        else:
            return None, 400
    def post(self, lat, lng):
        if not request.is_json: 
            return None, 400
        json=request.get_json()
        body=validate_bodyciot(json)

        if not body:
            return None, 400
        
        return_value=canile.insert_info_ciot(lat, lng,**body)

        if return_value=='ok':
            return None, 201
        else: 
            return None, 404



api.add_resource(animal, f'{basePath}/animale/<string:animale>')
api.add_resource(posizione, f'{basePath}/posizione/<string:long>/<string:lat>/<string:tipo>')
api.add_resource(mangiato, f'{basePath}/mangiato/<string:animale>')
api.add_resource(info, f'{basePath}/info/<string:animale>')
api.add_resource(login, f'{basePath}/login/<string:username>/<string:password>')
api.add_resource(list, f'{basePath}/list')
api.add_resource(dftest, f'{basePath}/dftest')
api.add_resource(ml, f'{basePath}/ml/<string:lat>/<string:lng>')
api.add_resource(ciotola, f'{basePath}/ciotola/<string:lat>/<string:lng>')
api.add_resource(test, f'{basePath}/test/<string:long>/<string:lat>/<string:tipo>')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
