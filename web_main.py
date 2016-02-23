# encoding: utf8
__author__ = 'brianyang'

from flask import Flask, redirect
from view import blog
from service import Session
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from modelview import ArticleView, TagView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import rediscli
from model import Category
import redis
import sys
import os

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

path = os.path.join(os.path.dirname(__file__), 'static/backup')
admin.add_view(FileAdmin(path, '/static/backup/', name="备份文件"))

app.secret_key = '\xbd$\x96\xb4\x80GYt"\x01\x9bk+"\x0c\xbd+\xc2\xf7A\xcb\xea\xee\x89/\xbe)4\xce-\xa3qbrian'


@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

# new relic 监控 newrelic.com
#import newrelic.agent

#newrelic.agent.initialize('newrelic.ini')

#app.run(host='0.0.0.0', port=1998, debug=True)
