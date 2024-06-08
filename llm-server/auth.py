from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': '用户名已存在'}), 400
    else:
        new_user = User(username=username)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': '注册成功，请登录'}), 201


@auth_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.verify_password(password):
        login_user(user)
        role = 'admin' if user.is_admin else 'user'
        return jsonify({'message': '登录成功', 'role': role}), 200
    else:
        return jsonify({'message': '登录失败，请检查用户名和密码'}), 401


@auth_bp.route('/logout', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': '登出成功'}), 200
