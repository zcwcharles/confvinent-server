from flask import Blueprint, send_from_directory, request, redirect
import os

is_dev = False

router = Blueprint('router', 'router')

def to_login_page():
  if request.url != 'http://confvinent.com:8000/':
    return redirect('http://confvinent.com:8000')
  return send_from_directory(os.path.abspath('./flaskr/assets/login'), 'index.html')

def to_main_page():
  if is_dev:
    return redirect('http://confvinent.com:3001/main')
  return redirect('http://confvinent.com:8000/main')

def handle_assets(app):
  @app.before_request
  def is_static():
    if request.path.startswith('/assets'):
      return send_from_directory(os.path.abspath('./flaskr'), request.path[1:])

@router.route('/main')
@router.route('/main/<module>')
def main_page(module):
  return send_from_directory(os.path.abspath('./flaskr/assets/main'), 'index.html')
