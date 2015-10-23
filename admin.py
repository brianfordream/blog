# encoding: utf8
__author__ = 'brianyang'

from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask.ext.basicauth import BasicAuth
from model import Article, Category, Session
from modelview import TagView

from flask_admin import Admin

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'coderbrian'
app.config['BASIC_AUTH_PASSWORD'] = 'yang199095()'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

session = Session()
admin = Admin(app, name='flask_admin', template_mode='bootstrap3')
admin.add_view(ModelView(Article, session))
admin.add_view(TagView(session))
admin.add_view(ModelView(Category, session))
app.secret_key = 'key'
session.close()
#app.run(host='0.0.0.0', port=1024, debug=True)
