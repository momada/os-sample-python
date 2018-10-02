import imp
import os
import sys

#from flask import Flask
#application = Flask(__name__)

#@application.route("/")
#def hello():
#    return "Hello World!"

#if __name__ == "__main__":
#    application.run()

#
#  main():
#
if __name__ == '__main__':
    application = imp.load_source('app', 'news/__init__.py')
    port = application.app.config['PORT']
    ip = application.app.config['IP']
    app_name = application.app.config['APP_NAME']
    host_name = application.app.config['HOST_NAME']

    try:
        imp.find_module('flask')
        fwtype = "flask"
    except ImportError:
        pass

    print('Starting WSGIServer type %s on %s:%d ... ' % (fwtype, ip, port))
    application.app.run(host=ip, port=port, debug=False)


