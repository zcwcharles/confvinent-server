import os
import shutil
from flask import Blueprint, jsonify, request, current_app
from uuid import uuid4
from ..db import execute_select_query, execute_modify_query
from .auth import get_user_id_by_session

submission = Blueprint('submission', 'submission', url_prefix='/api/submission')

@submission.route('/submissionlist', methods=['GET'])
def get_submission_list():
  user_id = get_user_id_by_session()
  res = execute_select_query(
    f'''
      select SUBMISSION.sub_id, CONFERENCE.submit_deadline, SUBMISSION.name, CONFERENCE.name as con_name, status from AUTHOR
      left join SUBMISSION on AUTHOR.sub_id=SUBMISSION.sub_id
      left join CONFERENCE on CONFERENCE.con_id=SUBMISSION.con_id
      where AUTHOR.user_id="{user_id}";
    '''
  )
  return jsonify({
    'message': 'ok',
    'data': {
      'submissionList': [{
        'subId': el['sub_id'],
        'name': el['name'],
        'conName': el['con_name'],
        'status': el['status']
      } for el in res]
    }
  })

@submission.route('/subid', methods=['GET'])
def get_sub_id():
  sub_id = str(uuid4())
  return jsonify({
    'message': 'ok',
    'data': {
      'subId': sub_id
    }
  })

@submission.route('/upload/<sub_id>', methods=['POST'])
def upload(sub_id):
  paper = request.files['paper']
  save_path = os.path.join(current_app.config['TEMP_FOLDER'], f'{sub_id}.pdf')
  if os.path.exists(save_path):
    os.remove(save_path)
  paper.save(save_path)
  return jsonify({
    'message': 'ok',
  })

def assign_reviewers(sub_id, con_id):
  res = execute_select_query(
    f'''
      select comit_id, review_number_for_each_paper from CONFERENCE
      where con_id="{con_id}"
    '''
  )
  num = res[0]['review_number_for_each_paper']
  comit_id = res[0]['comit_id']
  reviewer_list = execute_select_query(
    f'''
      select MEMBERS.user_id, cnt from MEMBERS left join (
        select distinct user_id, count(user_id) as cnt from REVIEW where decision is null group by user_id
      ) as DECISION_CNT on MEMBERS.user_id = DECISION_CNT.user_id
      where MEMBERS.comit_id="{comit_id}" and MEMBERS.comit_status="ACTIVE"
      order by cnt asc, cnt is null;
    '''
  )

  reviewer_id_list = ['("' + reviewer['user_id'] + f'", "{sub_id}", null)' for reviewer in reviewer_list[:num]]
  reviewer_id_query_str = (', ').join(reviewer_id_list)

  execute_modify_query(
    f'''
      insert into REVIEW
      values {reviewer_id_query_str};
    '''
  )


@submission.route('/submit/<sub_id>', methods=['POST'])
def create(sub_id):
  title, con_id, authors = request.json['title'], request.json['conId'], request.json['authors']
  execute_modify_query(
    f'''
      insert into SUBMISSION
      values ("{sub_id}", UNIX_TIMESTAMP(NOW()), "{title}", "PENDING", "{con_id}");
    '''
  )

  user_id_list = []

  for author in authors:
    email = author['email']
    res = execute_select_query(
      f'''
        select user_id from USER
        where email="{email}";
      '''
    )
    user_id_list.append(res[0]['user_id'])
  
  author_str_list = [f'("{user_id}", "{sub_id}")' for user_id in user_id_list]
  author_list_query = (', ').join(author_str_list)
  execute_modify_query(
    f'''
      insert into AUTHOR
      values {author_list_query};
    '''
  )

  temp_path = os.path.join(current_app.config['TEMP_FOLDER'], f'{sub_id}.pdf')
  targe_path = os.path.join(current_app.config['PAPER_FOLDER'], f'{sub_id}.pdf')
  shutil.move(temp_path, targe_path)

  assign_reviewers(sub_id, con_id)

  return jsonify({
    'message': 'ok'
  })

@submission.route('/get/<sub_id>', methods=['GET'])
def get(sub_id):
  sub_info = execute_select_query(
    f'''
      select * from SUBMISSION left join CONFERENCE on SUBMISSION.con_id=CONFERENCE.con_id
      where sub_id="sub_id";
    '''
  )

  authors_info = execute_select_query(
    f'''
      select first_name, last_name, email
      from AUTHOR left join USER on AUTHOR.user_id=USER.user_id
      where sub_id="{sub_id}";

    '''
  )

  authors = [{
    'firstName': author['first_name'],
    'lastName': author['last_name'],
    'email': author['email']
  } for author in authors_info]

  sub = {
    'title': sub_info[0]['title'],
    'conName': sub_info[0]['name'],
    'authors': authors
  }

  return jsonify({
    'message': 'ok',
    'data': sub
  })
