import os
import tempfile
import shutil
import atexit
from flask import Flask
from flask_cors import CORS
from .db import db
from .modules import *
from .router import handle_assets, router

tmp_folder = tempfile.mkdtemp(dir=os.getcwd())

def before_exit():
  shutil.rmtree(tmp_folder)

atexit.register(before_exit)

def create_app():
  app = Flask('confvinent')
  app.config['MYSQL_HOST'] = 'localhost'
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = 'abc123'
  app.config['MYSQL_DB'] = 'confvinent'
  app.config['SERVER_NAME'] = 'confvinent.com:8000'
  app.config['PAPER_FOLDER'] = f'{os.getcwd()}/papers'
  app.config['TEMP_FOLDER'] = tmp_folder

  CORS(app, origins='*', supports_credentials=True)
  db.init_app(app)
  handle_assets(app)
  init_auth(app)

  app.register_blueprint(router)
  app.register_blueprint(auth)
  app.register_blueprint(privilege)
  app.register_blueprint(committee)
  app.register_blueprint(conference)
  app.register_blueprint(submission)
  app.register_blueprint(review)
  app.register_blueprint(requests)

  return app
