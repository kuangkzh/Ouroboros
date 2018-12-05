import http.server
import RequestHandler
import config
import os


config.DEFAULT_ROOT = os.path.abspath(config.DEFAULT_ROOT)
os.chdir(config.DEFAULT_ROOT)

x = http.server.HTTPServer(('', config.PORT), RequestHandler.RequestHandler)
x.serve_forever()
