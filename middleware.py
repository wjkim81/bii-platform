from flask import request
from werkzeug.wrappers import Request

def check_ip(request):
    remote_ip = request.remote_addr
    return remote_ip

class IPCheckerMiddleware(object):
    def __init__(self, app):

        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)
        remote_ip = check_ip(request)
        print("remote_ip:", remote_ip)
        return self.app(environ, start_response)
