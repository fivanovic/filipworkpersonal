from flask import Flask
from flask_restplus import Api, Resource, fields
import requests
#import lib8relind
import pigpio
pi = pigpio.pi()

app = Flask(__name__)
api = Api(app, version='1.0',title='RELAY SWITCH',description='a RESTfl api to control the basic 3 relay board',doc='/docs')

ns = api.namespace('pins', description='Pin related operations')

pin_model = api.model('pins', {
    'id': fields.Integer(readonly=True, description='pin unique identifier'),
    'pin_num': fields.Integer(required=True, description='gpio pin number'),
    'use': fields.String(required=True, description='what the pin is being used for'),
    'state': fields.String(required=True, description='Pin on or off'),
    'button': fields.Integer(required=True, description='related button')
})

class PinUtil(object):
    def __init__(self):
        self.counter = 0
        self.pins = []

    def get(self, id):
        for pin in self.pins:
            if pin['id'] == id:
                return pin
        api.abort(404, f"pin {id} does not exist.")

    def create(self, data):
        pin = data
        pin['id'] = self.counter = self.counter + 1
        self.pins.append(pin)
        pi.set_mode(pin['pin_num'],pigpio.OUTPUT)

        if pin['state'] == 'off':
            pi.write(pin['pin_num'],1)
            pi.write(pin['button'],0)
        elif pin['state'] == 'on':
            pi.write(pin['pin_num'],0)
            pi.write(pin['button'],1)

        return pin

    def update(self, id, data):
        pin = self.get(id)
        pin.update(data) #this is the dict object update method
        pi.set_mode(pin['pin_num'],pigpio.OUTPUT)

        if pin['state'] == 'off':
            pi.write(pin['pin_num'],1)
            pi.write(pin['button'],0)
        elif pin['state'] == 'on':
            pi.write(pin['pin_num'],0)
            pi.write(pin['button'],1)

        return pin

    def delete(self,id):
        pin = self.get(id)
        pi.write(pin['pin_num'],0)
        self.pins.remove(pin)

@ns.route('/') #this is using the pins namespace
class PinList(Resource):
    """shows a list of all pins, lets you POST to add new pins"""

    #@ns.marshal_list_with(pin_model)
    #def get(self):
        #"""list all pins"""
        #return pin_util.pins

    #@ns.expect(pin_model)
    #@ns.marshal_with(pin_model, code=201)
    #def post(self):
        #"""create a new pin"""
        #return pin_util.create(api.payload)

@ns.route('/<int:id>')
@ns.response(404, 'pin not found')
@ns.param('id', 'the pin identifier')
class Pin(Resource):
    """shows a single pin item and lets you update/delete"""

    #@ns.marshal_with(pin_model)
    #def get(self, id):
        #"""fetch a pin given its identifier"""
        #return pin_util.get(id)

    #@ns.response(204, 'pin deleted')
    #def delete(self,id):
        #"""delete a pin given it identifier"""
        #pin_util.delete(id)
        #return '', 204

    #@ns.expect(pin_model, validate=True)
    #@ns.marshal_with(pin_model)
    #def put(self, id):
        #"""update a pin given its identifier"""
        #return pin_util.update(id, api.payload)

    @ns.expect(pin_model.'state')
    @ns.marshal_with(pin_model, mask='state')
    def patch(self, id):
        """partially update a pin given its identifier"""
        return pin_util.update(id, api.payload)

pin_util = PinUtil()
pin_util.create({'pin_num': 26, 'use': 'relay', 'state': 'off', 'button': 2})
pin_util.create({'pin_num': 20, 'use': 'relay', 'state': 'off', 'button': 3})
pin_util.create({'pin_num': 21, 'use': 'relay', 'state': 'off', 'button': 4})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
