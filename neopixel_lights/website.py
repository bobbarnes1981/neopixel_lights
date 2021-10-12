import json
import os
import web

from lights import Lights

render = web.template.render(os.path.dirname(__file__) + '/templates/')

lights = Lights()

class Website(object):
    def __init__(self):
        urls = (
            '/', 'index',
            '/api/colours', 'api_colours',
            '/api/brightness', 'api_brightness',
        )
        self.app = web.application(urls, globals())
    def start(self):
        lights.start()
        self.app.run()

class index(object):
    def GET(self):
        return render.index(lights)

class api_colours(object):
    def GET(self):
        return json.dumps({'colours': lights.colours})

class api_brightness(object):
    def GET(self):
        return json.dumps({'brightness': lights.brightness})
    def PUT(self):
        data = json.loads(web.data())
        # TODO: validate brightness 0.0 - 1.0
        lights.brightness = float(data['brightness'])
        lights.create()
        return json.dumps({'brightness': lights.brightness})

