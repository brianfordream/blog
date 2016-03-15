# encoding:utf8
__author__ = 'brianyang'

from flask import Blueprint, request
from datetime import datetime
import json

ionic = Blueprint('ionic', __name__, url_prefix='/ionic')


@ionic.route('/sendmsg', methods=['POST'])
def send_message():
    params = request.json
    msg = 'hello' + params.get('message')
    return msg

@ionic.route('/get_info', methods=['GET'])
def get_info():
    msg = [{
        'id':1,
        'title':"hello world",
        'desc':'hello this is a test fileaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'time': str(datetime.now()),
        'url': 'http://www.qunar.com'
    },
         {
             'id':2,
        'title':"hello world",
        'desc':'hello this is a test file',
        'time': str(datetime.now()),
        'url': 'http://www.qunar.com'
    },{
            'id':3,
        'title':"hello world",
        'desc':'hello this is a test fileaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'time': str(datetime.now()),
        'url': 'http://www.qunar.com'
    },
         {
             'id':4,
        'title':"hello world",
        'desc':'hello this is a test file',
        'time': str(datetime.now()),
        'url': 'http://www.qunar.com'
    }
    ]
    return json.dumps(msg)

