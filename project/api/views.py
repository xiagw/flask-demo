# project/api/views.py
from sqlalchemy import exc
from project.api.models import User
from project import db
from flask import Blueprint, jsonify, request, render_template

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    # 获取POST的数据
    post_data = request.get_json()
    if not post_data:
        response_data = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_data), 400
    email = post_data.get('email')
    username = post_data.get('username')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            # 证明数据库中不存在该email的用户，可以添加
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_data = {
                'status': 'success',
                'message': '%s was added!' % email
            }
            return jsonify(response_data), 201
        # 证明该email已经存在
        response_data = {
            'status': 'fail',
            'message': 'Sorry. That email already exists.'
        }
        return jsonify(response_data), 400
    except exc.IntegrityError as e:
        db.session.rollback()  # 出现异常了，回滚
        response_data = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_data), 400
