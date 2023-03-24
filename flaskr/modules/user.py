from flask import Blueprint, request
from uuid import uuid4
from ..router import to_main_page
from ..db import db

user = Blueprint('user', 'user', url_prefix='/api/user')

@user.route('/signup', methods=['POST'])
def signup():
    user_id = str(uuid4())
    first_name, last_name, address, organization, email, password = \
      request.json['firstName'], request.json['lastName'], request.json['address'],\
        request.json['organization'], request.json['email'], request.json['password']

    cursor = db.connection.cursor()
    cursor.execute(
      f'''
        insert into USER
        values ('{user_id}', '{email}', '{password}', '{first_name}', '{last_name}', '{address}', '{organization}');
      ''')
    cursor.close()

    return to_main_page()
