import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

db = SQLAlchemy(app)

from backend.models import *
from backend.db_seed import seed

with app.app_context():
    db.create_all()
    db.session.commit()
    seed()

from backend.routes import *

