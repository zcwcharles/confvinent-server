from flask import Flask
from flask_cors import CORS
from .db import db
from .modules import *
from .router import handle_assets, router

def create_app():
  app = Flask('confvinent')
  app.config['CORS_HEADERS'] = 'Content-Type'
  app.config['MYSQL_HOST'] = 'localhost'
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = 'abc123'
  app.config['MYSQL_DB'] = 'confvinent'

  CORS(app, origins=['*'])
  db.init_app(app)
  handle_assets(app)
  init_auth(app)

  app.register_blueprint(test)

  app.register_blueprint(router)
  app.register_blueprint(auth)
  app.register_blueprint(user)

  return app
