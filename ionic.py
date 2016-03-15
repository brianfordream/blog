# encoding:utf8
__author__ = 'brianyang'

from flask import Blueprint, request
import json

ionic = Blueprint('ionic', __name__, url_prefix='/ionic')


@ionic.route('/sendmsg', methods=['POST'])
def send_message():
    params = request.json
    msg = 'hello' + params.get('message')
    return msg

