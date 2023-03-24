from flask import request, session, redirect, jsonify, Blueprint
from flask_session import Session
import datetime
from ..router import to_login_page, to_main_page

LIFE_TIME = datetime.timedelta(days=1)

def is_auth():
  return session.get(request.cookies.get('_auth'))

def init_auth(app):
  add_auth_check(app)
  init_session(app)

  @app.route('/')
  def homepage():
    if is_auth():
      return to_main_page()
    return to_login_page()

def add_auth_check(app):
  @app.before_request
  def check_auth_before_request():
    if request.path != '/' and not request.path.startswith('/api/auth') and request.path != '/api/user/signup':
      if not is_auth():
        return to_login_page()

def init_session(app):
  app.config['SECRET_KEY'] = '81a499e9-09b8-4fe5-8176-2dc4a5f430e6'
  app.config['SESSION_COOKIE_NAME'] = '_auth'
  app.config['PERMANENT_SESSION_LIFETIME'] = LIFE_TIME
  app.config['SESSION_TYPE'] = 'filesystem'

  Session(app)

auth = Blueprint('auth', 'auth', url_prefix='/api/auth')

@auth.route('/signin', methods=['POST'])
def signin():
  try:
    if not request.json['email'] or not request.json['password']:
      resp = jsonify({'message': 'bad request'})
      resp.status_code = 400
      return resp
    id = 'aaaa'
    session[id] = request.json['email']
    resp = jsonify({'message': 'ok'})
    resp.set_cookie('_id', id, LIFE_TIME, httponly=True)
    return resp
  except Exception as err:
    print(err)
    resp = jsonify({'message': 'unknown error'})
    resp.status_code = 500
    return resp

@auth.route('/logout', methods=['DELETE'])
def logout():
  id = request.cookies.get('_id')
  if session.get(id):
    del session[id]
  
  return to_login_page()
