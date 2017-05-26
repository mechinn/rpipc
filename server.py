# sample.py
import falcon
import json
import rpipc 
from pprint import pprint

class ServersResource:
    def on_get(self, req, resp):
        resp.body = json.dumps(rpipc.servers)

class ServerResource:
    actions = {
        'poweron': rpipc.poweron,
        'poweroff': rpipc.poweroff,
        'reset': rpipc.reset,
        'kill': rpipc.kill,
    }
    def get_status(self,name):
        return json.dumps({
            'power': 'on' if rpipc.status(name) else 'off'
        })

    def on_get(self, req, resp, name):
        resp.body = self.get_status(name)

    def on_post(self, req, resp, name):
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)
 
        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Malformed JSON',
                'Could not decode the request body. The JSON was incorrect.')

        try:
            action = self.actions.get(result_json['action'])
            action(name)
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing action',
                'Needs to include one of the following actions: {}'.format(self.actions.keys()))
        
        resp.body = self.get_status(name)
 
api = falcon.API()
api.add_route('/', ServersResource())
api.add_route('/server/{name}', ServerResource())
