from flask import Blueprint, jsonify, request
from uuid import uuid4
from .auth import get_user_id_by_session
from ..db import execute_select_query, execute_modify_query

committee = Blueprint('committee', 'committee', url_prefix='/api/committee')

def get_comit_id_by_user_id(user_id):
  res = execute_select_query(
    f'''
      select comit_id from MEMBERS
      where user_id="{user_id}";
    '''
  )
  return '' if not res else res[0]['comit_id']

@committee.route('/committeeinfo', methods=['GET'])
def get_committee_info():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  [committee] = execute_select_query(
    f'''
      select * from COMMITTEE
      where comit_id="{comit_id}";
    '''
  )
  memebers = execute_select_query(
    f'''
      select user_id from MEMBERS
      where comit_id="{comit_id}";
    '''
  )
  resp = jsonify({
    'message': 'ok',
    'data': {
      'committee': committee,
      'members': [el['user_id'] for el in memebers],
    }
  })
  return resp

@committee.route('/addmember', methods=['POST'])
def add_member():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  post_user_id = request.json['userId']
  execute_modify_query(
    f'''
      insert into MEMBERS
      values ("{post_user_id}", "{comit_id}", "ACTIVE");
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/inactivate', methods=['POST'])
def inactivate_member():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  post_user_id = request.json['userId']
  execute_modify_query(
    f'''
      update MEMBERS
      set comit_status="INACTIVE"
      where user_id="{post_user_id}" and comit_id="{comit_id}";
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/activate', methods=['POST'])
def activate_member():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  post_user_id = request.json['userId']
  execute_modify_query(
    f'''
      update MEMBERS
      set comit_status="ACTIVE"
      where user_id="{post_user_id}" and comit_id="{comit_id}";
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/deletemember', methods=['POST'])
def delete_member():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  post_user_id = request.json['userId']
  execute_modify_query(
    f'''
      delete from MEMBERS
      where user_id="{post_user_id}" and comit_id="{comit_id}";
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/addadmin', methods=['POST'])
def add_admin():
  user_id = request.json['userId']
  comit_id = request.json['comitId']
  execute_modify_query(
    f'''
      insert into ADMINS
      values ("{user_id}", "{comit_id}")
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/deleteadmin', methods=['POST'])
def delete_admin():
  user_id = request.json['userId']
  comit_id = request.json['comitId']
  execute_modify_query(
    f'''
      delete from ADMINS
      where user_id="{user_id}" and comit_id="{comit_id}"
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/addcommittee', methods=['POST'])
def add_committee():
  comit_id = str(uuid4())
  name, icon = request.json['name'], request.json['icon']
  execute_modify_query(
    f'''
      insert into COMMITTEE
      values ("{comit_id}", "{name}", "{icon}");
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/committees', methods=['GET'])
def get_committees():
  res = execute_select_query(
    f'''
      select * from COMMITTEE;
    '''
  )

  return jsonify({
    'message': 'ok',
    'data': {
      'committees': [{
        'id': el['comit_id'],
        'name': el['name'],
      } for el in res]
    }
  })