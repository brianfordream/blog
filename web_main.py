# encoding: utf8
__author__ = 'brianyang'

from flask import Flask
from view import blog

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.debug=True

app.register_blueprint(blog)
app.run(host='0.0.0.0', port=1998, debug=True)
