import json
import os
import web

from lights import Lights
from web.httpserver import StaticMiddleware

render = web.template.render(os.path.dirname(__file__) + '/templates/')

lights = Lights()

class Website(object):
    def __init__(self):
        urls = (
            '/', 'index',
            '/api/colours', 'api_colours',
            '/api/selectedcolours', 'api_selectedcolours',
            '/api/brightness', 'api_brightness',
            '/api/shutdown', 'api_shutdown',
        )
        self.app = web.application(urls, globals())
    def start(self):
        lights.start()
        self.app.run(lambda app: StaticMiddleware(app, '/content/', os.path.dirname(__file__)))

class index(object):
    def GET(self):
        return render.index(lights, {'c': 'Christmas', 'h': 'Halloween'}, lights.chase_selected_colours)

class api_colours(object):
    def GET(self):
        return json.dumps({'colours': lights.chase_colours})

class api_selectedcolours(object):
    def GET(self):
        return json.dumps({'selected': lights.chase_selected_colours, 'colours': lights.chase_colours[lights.chase_selected_colours]})
    def PUT(self):
        data = json.loads(web.data())
        c = data['selected']
        if c in lights.chase_colours.keys():
            lights.chase_selected_colours = c
            lights.create()
        return json.dumps({'selected': lights.chase_selected_colours, 'colours': lights.chase_colours[lights.chase_selected_colours]})

class api_brightness(object):
    def GET(self):
        return json.dumps({'brightness': lights.brightness})
    def PUT(self):
        data = json.loads(web.data())
        b = float(data['brightness'])
        if b >= 0.0 and b <= 1.0:
            lights.brightness = b
            lights.create()
        return json.dumps({'brightness': lights.brightness})

class api_shutdown(object):
    def PUT(self):
        data = json.loads(web.data())
        if data['shutdown'] == 1:
            lights.set_mode('off')
            os.system('shutdown -h now')
        return json.dumps({'shutdown': 1})

