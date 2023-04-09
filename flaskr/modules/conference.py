from flask import Blueprint, jsonify, request
from uuid import uuid4
from ..db import execute_select_query, execute_modify_query
from .committee import get_comit_id_by_user_id
from .auth import get_user_id_by_session

conference = Blueprint('conferencce', 'conferencce', url_prefix='/api/conferencce')

@conference.route('/create', methods=['POST'])
def create():
  con_id = str(uuid4())
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  name, submit_deadline, review_deadline, review_number_for_each_paper, end_time \
    = request.json['name'], request.json['submitDeadline'], request.json['reviewDeadline'], \
      request.json['reviewNumberForEachPaper'], request.json['endTime']

  execute_modify_query(
      f'''
        insert into CONFERENCE
        values(
          "{con_id}","{name}", {submit_deadline}, {review_deadline},
          "{review_number_for_each_paper}", "{comit_id}", UNIX_TIMESTAMP() * 1000, {end_time}
        );
      '''
  )

  return jsonify({
    'message': 'ok'
  })

@conference.route('/currentconference', methods=['GET'])
def get_current_conference():
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  res = execute_select_query(
    f'''
      select * from CONFERENCE
      where end_time > UNIX_TIMESTAMP() * 1000 and comit_id="{comit_id}";
    '''
  )
  if not res:
    return jsonify({
      'message': 'ok',
    })
  return jsonify({
    'message': 'ok',
    'data': {
      'conId': res[0]['con_id'],
      'name': res[0]['name'],
      'submitDeadline': res[0]['submit_deadline'],
      'reviewDeadline': res[0]['review_deadline'],
      'reviewNumberForEachPaper': res[0]['review_number_for_each_paper'],
      'createTime': res[0]['create_time'],
      'endTime': res[0]['end_time']
    }
  })

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
  user_id = get_user_id_by_session()
  comit_id = get_comit_id_by_user_id(user_id)
  res = []
  if comit_id:
    res = execute_select_query(
      f'''
        select con_id, name from CONFERENCE
        where submit_deadline > UNIX_TIMESTAMP() * 1000 and comit_id != "{comit_id}";
      '''
    )
  else:
    res = execute_select_query(
      f'''
        select con_id, name from CONFERENCE
        where submit_deadline > UNIX_TIMESTAMP() * 1000;
      '''
    )

  return jsonify({
    'message': 'ok',
    'data': {
      'submitList': [{
        'conId': el['con_id'],
        'name': el['name']
      } for el in res]
    }
  })
