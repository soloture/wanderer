from flask import Flask
from flask import request, url_for, render_template
from flaskext.mongoalchemy import MongoAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MongoAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)
