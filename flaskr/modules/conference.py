from flask import Blueprint, jsonify, request
from uuid import uuid4
from ..db import execute_select_query, execute_modify_query
from .committee import get_comit_id_by_user_id

conference = Blueprint('conferencce', 'conferencce', url_prefix='/api/conferencce')

@conference.route('/create', methods=['POST'])
def create():
  con_id = str(uuid4())
  name, submit_deadline, review_deadline, review_number_for_each_paper, comit_id, create_time, end_time \
    = request.json['name'], request.json['submitDeadline'], request.json['reviewDeadline'], \
      request.json['reviewNumberForEachPaper'], request.json['comitId'], request.json['createTime'], \
      request.json['endTime']

  execute_modify_query(
      f'''
        insert into table CONFERENCE
        values(
          "{con_id}","{name}", "{submit_deadline}", "{review_deadline}",
          "{review_number_for_each_paper}", "{comit_id}", "{create_time}", "{end_time}"
        );
      '''
  )

  return jsonify({
    'message': 'ok'
  })

@conference.route('/getcurrentconference', methods=['GET'])
def get_current_conference():
  user_id = request.cookies.get('_id')
  comit_id = get_comit_id_by_user_id(user_id)
  res = execute_select_query(
    f'''
      select * from CONFERENCE
      where end_time > UNIX_TIMESTAMP(NOW()) and comit_id="{comit_id}";
    '''
  )
  if not res:
    return jsonify({
      'message': 'empty'
    })
  return jsonify(res[0])

@conference.route('/delete', methods=['POST'])
def delete():
  con_id = request.json['conId']

  execute_modify_query(
    f'''
      delete from CONFERENCE
      where con_id="{con_id}";
    '''
  )

  return jsonify({
    'message': 'ok'
  })

@conference.route('/submitlist', methods=['GET'])
def submit_list():
  user_id = request.cookies.get('_id')
  comit_id = get_comit_id_by_user_id(user_id)
  res = []
  if comit_id:
    res = execute_select_query(
      f'''
        select con_id, name from CONFERENCE
        where submit_deadline > UNIX_TIMESTAMP(NOW()) and comit_id != "{comit_id}";
      '''
    )
  else:
    res = execute_select_query(
      f'''
        select con_id, name from CONFERENCE
        where submit_deadline > UNIX_TIMESTAMP(NOW());
      '''
    )

  return jsonify(res)