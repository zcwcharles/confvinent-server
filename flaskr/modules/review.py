import os
from flask import Blueprint, jsonify, send_from_directory, request, current_app
from ..db import execute_select_query, execute_modify_query
from .auth import get_user_id_by_session

DECISIONS = {
  'approve': 'APPROVED',
  'decline': 'DECLINED'
}

review = Blueprint('review', 'review', url_prefix='/api/review')

@review.route('/reviewlist', methods=['GET'])
def get_review_list():
  user_id = get_user_id_by_session()
  res = execute_select_query(
    f'''
      select REVIEW.sub_id, CONFERENCE.name as conName, review_deadline, title, status, decision from REVIEW
      left join SUBMISSION on SUBMISSION.sub_id = REVIEW.sub_id
      left join CONFERENCE on CONFERENCE.con_id = SUBMISSION.con_id
      where user_id="{user_id}";
    '''
  )

  return jsonify({
    'message': 'ok',
    'data': {
      'reviews': [{
        'subId': review['sub_id'],
        'reviewDeadline': review['review_deadline'],
        'title': review['title'],
        'status': review['status'],
        'conName': review['conName'],
        'decision': review['decision'],
      } for review in res]
    }
  })

@review.route('/get/<sub_id>', methods=['GET'])
def get_review(sub_id):
  send_from_directory(os.path.join(current_app.config['PAPER_FOLDER'], f'{sub_id}.pdf'))

@review.route('/submit/<sub_id>', methods=['POST'])
def submit_review(sub_id):
  user_id = get_user_id_by_session()

  decision = DECISIONS.get(request.json['decision'])

  if decision:
    execute_modify_query(
      f'''
        update REVIEW
        set decision="{decision}"
        where user_id="{user_id}" and sub_id="{sub_id}";
      '''
    )
  
  res = execute_select_query(
    f'''
      select decision from REVIEW
      where sub_id="{sub_id}";
    '''
  )

  approved = 0
  declined = 0

  for el in res:
    if el['decision'] == DECISIONS['approve']:
      approved += 1
    elif el['decision'] == DECISIONS['decline']:
      declined += 1
  
  if approved > len(res) // 2:
    execute_modify_query(
      f'''
        update SUBMISSION
        set status="APPROVED"
        where sub_id="{sub_id}";
      '''
    )
  elif declined > len(res) // 2:
    execute_modify_query(
      f'''
        update SUBMISSION
        set status="DECLINED"
        where sub_id="{sub_id}";
      '''
    )

  return jsonify({
    'message': 'ok'
  })
