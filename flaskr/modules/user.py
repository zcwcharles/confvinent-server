from flask import Blueprint, request
from uuid import uuid4
from ..router import to_main_page
from ..db import execute_select_query, execute_modify_query

user = Blueprint('user', 'user', url_prefix='/api/user')

@user.route('/signup', methods=['POST'])
def signup():
  user_id = str(uuid4())
  first_name, last_name, address, organization, email, password = \
    request.json['firstName'], request.json['lastName'], request.json['address'],\
      request.json['organization'], request.json['email'], request.json['password']

  execute_modify_query(
    f'''
      insert into USER
      values ('{user_id}', '{email}', '{password}', '{first_name}', '{last_name}', '{address}', '{organization}');
    '''
  )

  return to_main_page()

def get_user_id_by_email_and_pwd(email, password):
  return execute_select_query(
    f'''
      select user_id from USER
      where email="{email}" and password="{password}";
    '''
  )