import os
from flask import Blueprint, jsonify, request, current_app
from uuid import uuid4
from ..db import execute_select_query

submission = Blueprint('submission', 'submission', url_prefix='/api/submission')

@submission.route('/getsubmissionlist', methods=['GET'])
def get_submission_list():
  user_id = request.cookies.get('_id')
  res = execute_select_query(
    f'''
      select SUBMISSION.sub_id, CONFERENCE.submit_deadline, SUBMISSION.name, CONFERENCE.name as con_name, status from AUTHOR
      left join SUBMISSION on AUTHOR.sub_id=SUBMISSION.sub_id
      left join CONFERENCE on CONFERENCE.con_id=SUBMISSION.con_id
      where AUTHOR.user_id="{user_id}";
    '''
  )
  return jsonify([{
    'subId': el['sub_id'],
    'name': el['name'],
    'conName': el['con_name'],
    'status': el['status']
  } for el in res])

@submission.route('/upload', methods=['POST'])
def upload():
  paper = request.files['paper']
  sub_id = str(uuid4())
  paper.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f'{sub_id}.pdf'))
  return jsonify({
    'message': 'ok',
    'subId': sub_id
  })

# @submission.route('/create', methods=['POST'])
# def create():
#   sub_id, title, con_id, file_id
