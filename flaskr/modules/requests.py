from flask import Blueprint, jsonify, request
from uuid import uuid4
from ..db import execute_select_query, execute_modify_query

DECISION = {
  'approve': 'APPROVE',
  'decline': 'DECLINE'
}

requests = Blueprint('requests', 'requests', url_prefix='/api/requests')

@requests.route('/requestlist', methods=['GET'])
def get_request_list():
  user_id = request.cookies.get('_id')
  res = execute_select_query(
    f'''
      select MEMBERS.comit_id, ADMINS.comit_id as manage_comit_id from MEMBERS
      left join ADMINS on MEMBERS.user_id=ADMINS_ID.user_id
      where MEMBERS.user_id="{user_id}";
    '''
  )

  res = []
  comit_id = res[0]['comit_id']

  if res[0]['manage_comit_id']:
    res = execute_select_query(
      f'''
        select req_id, create_time, email, status, make_by from REQUEST
        left join USER on REQUEST.make_by = USER.user_id
        where comit_id="{comit_id}";
      '''
    )

    return jsonify({
      'message': 'ok',
      'data': {
        'requestList': [{
          'reqId': el['req_id'],
          'createTime': el['create_time'],
          'email': el['email'],
          'status': el['status'],
          'canProcess': el['make_by'] != user_id and el['status'] == 'PENDING'
        } for el in res]
      }
    })
  else:
    res = execute_select_query(
      f'''
        select req_id, create_time, email, status, from REQUEST
        left join USER on REQUEST.make_by = USER.user_id
        where make_by="{user_id}";
      '''
    )

    return jsonify({
      'message': 'ok',
      'data': {
        'requestList': [{
          'reqId': el['req_id'],
          'createTime': el['create_time'],
          'email': el['email'],
          'status': el['status'],
          'canProcess': False
        } for el in res]
      }
    })

@requests.route('/get/<req_id>')
def get_request(req_id):
  res = execute_select_query(
    f'''
      select * from REQUEST
      left join USER on REQUEST.make_by = USER.user_id
      where req_id="{req_id}";
    '''
  )

  return jsonify({
    'message': 'ok',
    'data': {
      'createTime': res['create_time'],
      'status': res['status'],
      'email': res['email'],
      'reason': res['reason']
    }
  })

@requests.route('/submit')
def submit_request():
  req_id = str(uuid4())
  user_id = request.cookies.get('_id')
  res = execute_select_query(
    f'''
      select comit_id from MEMBERS
      where user_id="{user_id}";
    '''
  )

  comit_id = res[0]['comit_id']
  
  reason = request.json['reason']

  execute_modify_query(
    f'''
      insert into REQUEST
      values ("{req_id}", "{comit_id}", UNIX_TIMESTAMP(NOW()), "PENDING", null, "{reason}", "{user_id}", null);
    '''
  )

  return jsonify({
    'message': 'ok'
  })

@requests.route('/process/<req_id>')
def process(req_id):
  user_id = request.cookies.get('_id')
  decison = DECISION.get(request.json['decision'])

  res = execute_select_query(
    f'''
      select status from REQUEST
      where req_id="{req_id}";
    '''
  )

  if decison and res[0]['status'] == 'PENDING':
    execute_modify_query(
      f'''
        update REQUEST
        set status="{decison}", process_by="{user_id}"
        where req="{req_id}";
      '''
    )
  
  return jsonify({
    'message': 'ok'
  })
