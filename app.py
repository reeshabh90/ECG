"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from ECG import app
from waitress import serve
import os

if __name__ == '__main__':
     
        #PORT=int(os.environ.get('PORT', 5000))
        PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
        #serve(app, port=PORT)
        PORT=8080
        serve(app, port=PORT)
        #set this command in heroku command
        #heroku config:add PORT=5000