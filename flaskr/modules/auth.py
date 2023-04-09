from flask import request, session, jsonify, Blueprint
from uuid import uuid4
import datetime
from ..router import to_login_page, to_main_page
from ..db import execute_select_query, execute_modify_query

LIFE_TIME = datetime.timedelta(days=1)

class RecordNotMatchError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)
    self.msg = 'The email or password did not match with our record.'

def get_user_id_by_session():
  return session.get('id')

def is_auth():
  return get_user_id_by_session()

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
    if request.path != '/' and not request.path.startswith('/api/auth') and request.method != 'OPTIONS':
      if not is_auth():
        return to_login_page()

def init_session(app):
  app.config['SECRET_KEY'] = '81a499e9-09b8-4fe5-8176-2dc4a5f430e6'
  app.config['SESSION_COOKIE_NAME'] = '_auth'
  app.config['PERMANENT_SESSION_LIFETIME'] = LIFE_TIME
  app.config['SESSION_REFRESH_EACH_REQUEST'] = False

auth = Blueprint('auth', 'auth', url_prefix='/api/auth')

def get_user_id_by_email_and_pwd(email, password):
  return execute_select_query(
    f'''
      select user_id from USER
      where email="{email}" and password="{password}";
    '''
  )

@auth.route('/signin', methods=['POST'])
def signin():
  try:
    if not request.json['email'] or not request.json['password']:
      resp = jsonify({'message': 'bad request'})
      resp.status_code = 400
      return resp
    
    email, password = request.json['email'], request.json['password']
    res = get_user_id_by_email_and_pwd(email, password)

    if not res:
      raise RecordNotMatchError

    id = res[0]['user_id']

    session['id'] = id
    resp = to_main_page()
    return resp

  except RecordNotMatchError as err:
    print(err)
    resp = jsonify({'message': err.msg})
    resp.status_code = 401
    return resp

  except Exception as err:
    print(err)
    resp = jsonify({'message': 'unknown error'})
    resp.status_code = 500
    return resp

@auth.route('/logout', methods=['DELETE'])
def logout():
  id = get_user_id_by_session()
  if session.get(id):
    session.pop(id)
  
  return to_login_page()

@auth.route('/signup', methods=['POST'])
def signup():
  user_id = str(uuid4())
  first_name, last_name, organization, email, password = \
    request.json['firstName'], request.json['lastName'],\
      request.json['organization'], request.json['email'], request.json['password']

  address = '' if 'address' not in request.json else request.json['address']

  execute_modify_query(
    f'''
      insert into USER
      values ("{user_id}", "{email}", "{password}", "{first_name}", "{last_name}", "{address}", "{organization}");
    '''
  )

  session['id'] = user_id
  resp = to_main_page()

  return resp
