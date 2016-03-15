# encoding:utf8
__author__ = 'brianyang'

from flask import Blueprint, request
import json

ionic = Blueprint('ionic', __name__, url_prefix='/ionic')


@ionic.route('/sendmsg', methods=['POST'])
def send_message():
    params = request.form
    msg = params.get('message')
    return 'hello'+msg

