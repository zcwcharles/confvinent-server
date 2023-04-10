from flask import Blueprint, jsonify, request
from .auth import get_user_id_by_session
from ..db import execute_select_query

privilege = Blueprint('privilege', 'privilege', url_prefix='/api/privilege')

@privilege.route('/usergroup', methods=['GET'])
def get_user_group():
  user_id = get_user_id_by_session()
  res = execute_select_query(
    f'''
      select first_name, last_name, MEMBERS.user_id as is_member, ADMINS.user_id as is_admin, SUPERADMIN.user_id as is_superadmin, MEMBERS.comit_status="ACTIVE" as is_active
      from USER
      left join MEMBERS on USER.user_id=MEMBERS.user_id
      left join ADMINS on USER.user_id=ADMINS.user_id
      left join SUPERADMIN on USER.user_id=SUPERADMIN.user_id
      where USER.user_id="{user_id}";
    '''
  )

  group = 'user'
  if res[0]['is_member'] is not None and res[0]['is_active']:
    group = 'member'
  if res[0]['is_admin'] is not None:
    group = 'admin'
  if res[0]['is_superadmin'] is not None:
    group = 'superadmin'
  
  return jsonify({
    'message': 'ok',
    'data': {
      'userGroup': group,
      'name': (f'''{res[0]['first_name'][0]}{res[0]['last_name'][0]}''').upper()
    }
  })