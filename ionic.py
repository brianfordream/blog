# encoding:utf8
__author__ = 'brianyang'

from flask import Blueprint, request
from datetime import datetime
import json
from util import get_redis_client
redis_client = get_redis_client()

ionic = Blueprint('ionic', __name__, url_prefix='/ionic')


@ionic.route('/sendmsg', methods=['POST'])
def send_message():
    params = request.json
    msg = 'hello' + params.get('message')
    return msg


page_num = 5

@ionic.route('/get_info', methods=['GET'])
def get_info():
    params = request.args
    cur_page = int(params.get('cur_page', 0))
    msg = json.loads(redis_client.get('scrapy_info'))
    return json.dumps(msg[cur_page*page_num:(cur_page+1)*page_num])

@ionic.route('/get_info_by_id', methods=['GET'])
def get_info_by_id():
    params = request.args
    id_ = params.get('id', 0)
    id_dict = json.loads(redis_client.get('scrapy_id_dict'))
    return json.dumps(id_dict.get(id_))

