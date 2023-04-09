import MySQLdb
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

def get_user_id_by_email(email):
  res = execute_select_query(
    f'''
      select user_id from USER
      where email="{email}";
    '''
  )
  return '' if not res else res[0]['user_id']

@committee.route('/committeeinfo', methods=['GET'])
def get_committee_info():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  res = execute_select_query(
    f'''
      select * from COMMITTEE
      where comit_id="{comit_id}";
    '''
  )
  members = execute_select_query(
    f'''
      select USER.user_id, first_name, last_name, email, comit_status, ADMINS.comit_id from MEMBERS
      left join USER on MEMBERS.user_id=USER.user_id
      left join ADMINS on MEMBERS.user_id=ADMINS.user_id
      where MEMBERS.comit_id="{comit_id}" and MEMBERS.user_id!="{user_id}";
    '''
  )
  resp = jsonify({
    'message': 'ok',
    'data': {
      'committee': {
        'id': res[0]['comit_id'],
        'name': res[0]['name'],
      },
      'members': [{
        'id': el['user_id'],
        'name': f'''{el['first_name']} {el['last_name']}''',
        'email': el['email'],
        'status': el['comit_status'],
        'isAdmin': el['comit_id'] != None
      } for el in members],
    }
  })
  return resp

@committee.route('/committeeinfo/<comit_id>', methods=['GET'])
def get_committee_info_by_id(comit_id):
  [committee] = execute_select_query(
    f'''
      select * from COMMITTEE
      where comit_id="{comit_id}";
    '''
  )
  members = execute_select_query(
    f'''
      select USER.user_id, first_name, last_name, email, comit_status, ADMINS.comit_id from MEMBERS
      left join USER on MEMBERS.user_id=USER.user_id
      left join ADMINS on MEMBERS.user_id=ADMINS.user_id
      where MEMBERS.comit_id="{comit_id}";
    '''
  )

  resp = jsonify({
    'message': 'ok',
    'data': {
      'committee': {
        'id': committee['comit_id'],
        'name': committee['name'],
      },
      'members': [{
        'id': el['user_id'],
        'name': f'''{el['first_name']} {el['last_name']}''',
        'email': el['email'],
        'status': el['comit_status'],
        'isAdmin': el['comit_id'] != None
      } for el in members],
    }
  })
  return resp

@committee.route('/update/<comit_id>', methods=['POST'])
def update(comit_id):
  name = request.json['name']
  execute_modify_query(
    f'''
      update COMMITTEE
      set name="{name}"
      where comit_id="{comit_id}";
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/addmember/<comit_id>', methods=['POST'])
def add_member_by_commitee(comit_id):
  email = request.json['email']
  add_user_id = get_user_id_by_email(email)


  if not add_user_id:
    resp = jsonify({
      'message': 'no such user'
    })
    resp.status_code = 400
    return resp

  try:
    execute_modify_query(
      f'''
        insert into MEMBERS
        values ("{add_user_id}", "{comit_id}", "ACTIVE");
      '''
    )
    return jsonify({
      'message': 'ok'
    })
  except MySQLdb.IntegrityError as err:
    print(err)
    resp = jsonify({'message': 'This user is already a member.'})
    resp.status_code = 400
    return resp
  except Exception as err:
    print(err)
    resp = jsonify({'message': 'unknown error'})
    resp.status_code = 500
    return resp

@committee.route('/deactivate/<comit_id>', methods=['POST'])
def inactivate_member_by_comit_id(comit_id):
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

@committee.route('/activate/<comit_id>', methods=['POST'])
def activate_member_by_comit_id(comit_id):
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

@committee.route('/addadmin/<comit_id>', methods=['POST'])
def add_admin_by_committee(comit_id):
  user_id = request.json['userId']
  execute_modify_query(
    f'''
      insert into ADMINS
      values ("{user_id}", "{comit_id}")
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/deleteadmin/<comit_id>', methods=['POST'])
def delete_admin(comit_id):
  user_id = request.json['userId']
  execute_modify_query(
    f'''
      delete from ADMINS
      where user_id="{user_id}" and comit_id="{comit_id}"
    '''
  )
  return jsonify({
    'message': 'ok'
  })

@committee.route('/deleteadmin')
def delete_admin_by_committee():
  user_id = request.json['userId']
  comit_id = get_comit_id_by_user_id(user_id)

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
  name = request.json['name']
  execute_modify_query(
    f'''
      insert into COMMITTEE
      values ("{comit_id}", "{name}");
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

@committee.route('/deletecommittee', methods=['POST'])
def delete_committee():
  comit_id = request.json['comitId']

  execute_modify_query(
    f'''
      delete from COMMITTEE
      where comit_id="{comit_id}";
    ''' 
  )

  return jsonify({
    'message': 'ok'
  })
