from flask import Flask
from flask_restplus import Api, Resource, fields
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
    'state': fields.String(required=True, description='Pin on or off')
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
        elif pin['state'] == 'on':
            pi.write(pin['pin_num'],0)

        return pin

    def update(self, id, data):
        pin = self.get(id)
        pin.update(data) #this is the dict object update method
        pi.set_mode(pin['pin_num'],pigpio.OUTPUT)

        if pin['state'] == 'off':
            pi.write(pin['pin_num'],1)
        elif pin['state'] == 'on':
            pi.write(pin['pin_num'],0)

        return pin

    def delete(self,id):
        pin = self.get(id)
        pi.write(pin['pin_num'],0)
        self.pins.remove(pin)

@ns.route('/') #this is using the pins namespace


@ns.route('/<int:id>')
@ns.response(404, 'pin not found')
@ns.param('id', 'the pin identifier')
class Pin(Resource):
    """shows a single pin item and lets you update/delete"""
    
    @ns.expect(pin_model)
    @ns.marshal_with(pin_model)
    def patch(self, id):
        """partially update a pin given its identifier"""
        return pin_util.update(id, api.payload)

pin_util = PinUtil()
pin_util.create({'pin_num': 26, 'use': 'relay', 'state': 'off'})
pin_util.create({'pin_num': 20, 'use': 'relay', 'state': 'off'})
pin_util.create({'pin_num': 21, 'use': 'relay', 'state': 'off'})

pin_util.create({'pin_num': 2, 'use': 'button', 'state': 'off'})
pin_util.create({'pin_num': 3, 'use': 'button', 'state': 'off'})
pin_util.create({'pin_num': 4, 'use': 'button', 'state': 'off'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
