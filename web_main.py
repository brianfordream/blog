# encoding: utf8
__author__ = 'brianyang'

from flask import Flask, session, redirect, request
from view import blog
from service import Session
from flask_admin import Admin
from modelview import ArticleView, TagView
from flask_admin.contrib.sqla import ModelView
from model import Category
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.debug = True

app.register_blueprint(blog)

db_session = Session()
admin = Admin(app, name='flask_admin', template_mode='bootstrap3')
admin.add_view(ArticleView(db_session))
admin.add_view(TagView(db_session))
admin.add_view(ModelView(Category, db_session))


@app.route('/admin/login/', methods=['POST'])
def login():
    params = request.form
    name = params['name']
    password = params['password']
    if name == 'CoderBrian' and password == 'Yang199095()':
        session['admin'] = 'admin'
        return redirect('/admin/')
    else:
        return redirect('/admin/')

app.secret_key = '\xbd$\x96\xb4\x80GYt"\x01\x9bk+"\x0c\xbd+\xc2\xf7A\xcb\xea\xee\x89/\xbe)4\xce-\xa3qbrian'
app.run(host='0.0.0.0', port=1998, debug=True)
