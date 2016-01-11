# encoding: utf8
__author__ = 'brianyang'

from flask import Flask, redirect, url_for
from view import blog
from service import Session
from flask_admin import Admin
from modelview import ArticleView, TagView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import rediscli
from model import Category
import redis
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.debug = False

app.register_blueprint(blog)
session = Session()
admin = Admin(app, name='flask_admin', template_mode='bootstrap3')
admin.add_view(ArticleView(session))
admin.add_view(TagView(session))
admin.add_view(ModelView(Category, session))
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password='Djhd1234')
r = redis.StrictRedis(connection_pool=pool)
admin.add_view(rediscli.RedisCli(r))

app.secret_key = '\xbd$\x96\xb4\x80GYt"\x01\x9bk+"\x0c\xbd+\xc2\xf7A\xcb\xea\xee\x89/\xbe)4\xce-\xa3qbrian'


@app.errorhandler(404)
def page_not_found(error):
    try:
        return redirect('/')
    except Exception, e:
        logging.error(e)


app.run(host='0.0.0.0', port=1998, debug=True)
