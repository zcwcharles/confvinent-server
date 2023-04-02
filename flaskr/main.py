import os
from flask import Flask
from flask_cors import CORS
from .db import db
from .modules import *
from .router import handle_assets, router

def create_app():
  app = Flask('confvinent')
  app.config['MYSQL_HOST'] = 'localhost'
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = 'abc123'
  app.config['MYSQL_DB'] = 'confvinent'
  app.config['SERVER_NAME'] = 'confvinent.com:5000'
  app.config['UPLOAD_FOLDER'] = f'{os.getcwd()}/papers'

  CORS(app, origins='*', supports_credentials=True)
  db.init_app(app)
  handle_assets(app)
  init_auth(app)

  app.register_blueprint(router)
  app.register_blueprint(auth)
  app.register_blueprint(user)
  app.register_blueprint(committee)
  app.register_blueprint(conference)
  app.register_blueprint(submission)

  return app
