from flask import Blueprint, jsonify

test = Blueprint('test', 'test', url_prefix='/api/test')

@test.route('ping', methods=['GET', 'POST'])
def ping():
    
    return jsonify({
       'message': 'ok'
    })
