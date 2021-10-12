import os
import web

from lights import Lights

render = web.template.render(os.path.dirname(__file__) + '/templates/')

lights = Lights()

class Website(object):
    def __init__(self):
        urls = (
            '/', 'index'
        )
        self.app = web.application(urls, globals())
    def start(self):
        lights.start()
        self.app.run()

class index(object):
    def GET(self):
        return render.index(lights)

