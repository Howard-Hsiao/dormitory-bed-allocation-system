import flask
from flask import request
from flask import jsonify
from app import app

import time
# import resource
import sys
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from utility.static.Qua_config import *
from utility.Qua_mainFunc import *
from utility.save_result import *


@app.route('/api/get_all_identities/', methods = ['POST'])
def identityPool():
    if request.method == 'POST':
        time_start = time.clock()
        print('request', request)
        student_data = request.json
        identity_pool = GetAllIdType(student_data)
        time_elapsed = (time.clock() - time_start)
        print('identity_pool', identity_pool)
        print('time_elapsed', time_elapsed)
        # print('memory usage', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return jsonify(identity_pool)

@app.route('/api/match/', methods = ['POST'])
def result():
    if request.method == 'POST':
        time_start = time.clock()
        print('request', request)
        student = request.json['student']
        beds = request.json['beds']
        priority = request.json['priority']
        BoyInQua, GirlInQua, WaitDF = DivideDF(priority, student, beds)
        BoyInQua, GirlInQua = Match(BoyInQua, GirlInQua, beds)
        CampusBoy, CampusGirl, BotBoy, BotGirl = GetOutputDF(priority, BoyInQua, GirlInQua, student, WaitDF)
        
        result = {
            "men_campus_dorm": CampusBoy,
            "women_campus_dorm": CampusGirl,
            "men_BOT": BotBoy,
            "women_BOT": BotGirl,
        }

        time_elapsed = (time.clock() - time_start)
        print('time_elapsed', time_elapsed)
        # print('memory usage', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return jsonify(result)
    
@app.route('/api/save/', methods = ['POST'])
def save():
    if request.method == 'POST':
        print('request', request)
        file_path = request.json['file_path']
        men_campus_dorm = request.json['men_campus_dorm']
        women_campus_dorm = request.json['women_campus_dorm']
        men_BOT = request.json['men_BOT']
        women_BOT = request.json['women_BOT']
        result = {
            'men_campus_dorm': men_campus_dorm,
            'women_campus_dorm': women_campus_dorm,
            'men_BOT': men_BOT,
            'women_BOT': women_BOT,
        }
        saveExcel(result, file_path)
        
        result = {}
        return jsonify(result)
