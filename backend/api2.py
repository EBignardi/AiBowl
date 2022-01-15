from flask import Flask, request
from flask_restful import Resource, Api
from marketplace import marketplace
from uuid import UUID
from datetime import datetime
app=Flask(__name__)
api2=Api(app)
basePath='/api2/v1'
market=marketplace()


def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj=UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test
def validate_price(price):
        try: 
            float(price) 
        except ValueError:
            return False  
        if float(price)<0.01:
            return False
        return price

def validate_body(json):
    if 'price' not in json:
        return False
    else :
        p=json['price']
        try: 
            float(p) 
        except ValueError:
            return False  
        if float(p)<0.01:
            return False
        return json

    
class Market(Resource):

    def post(self,user,game):
        if not validate_uuid(user):
            return None, 400
        if not validate_uuid(game):
            return None, 400
        if not request.is_json: 
            return None, 400
        json=request.get_json()
        body=validate_body(json)

        if not body:
            return None, 400
        
        return_value=market.get_info(user, game)
        if not return_value:
            return None, 409
        
        return_value=market.modify_price(user,game,**body)

        if return_value=='ok':
            return None, 201
        else: 
            return None, 400

        


api2.add_resource(Market, f'{basePath}/game/<string:user>/<string:game>')
if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
