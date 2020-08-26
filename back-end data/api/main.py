import flask
from flask import request
from flask import jsonify
import json
import argparse
import sys
import logging
from app import app


sys.stdout = open('flask_out.txt', 'w')
sys.stderr = open('flask_err.txt', 'w')
log = logging.getLogger('werkzeug')
log.disabled = True

def import_router():
    import router.router

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug")
    args = parser.parse_args() 
    
    if args.debug:
        app.debug = True

    import_router()
    app.run(debug=app.debug)