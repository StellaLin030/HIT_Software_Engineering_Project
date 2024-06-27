import re
import random
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db, redis_conn
from sendEmail import send_mail

auth_bp = Blueprint('auth', __name__)


# 发送验证码
@auth_bp.route('/authenticate', methods=['POST'])
@cross_origin(supports_credentials=True)
def authenticate():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    # 邮箱匹配正则
    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
        return jsonify({'message': '请填写正确的邮箱'}), 400
    # user_email = User.query.filter_by(email=email).first()
    if User.query.filter_by(email=email).first():
        return jsonify({'message': '邮箱已被注册'}), 400

    # 生成验证码
    authcode = '%06d' % random.randint(0, 99999)
    print('邮箱验证码为: ' + authcode)
    redis_conn.set('AUTHCODE:' + email, authcode, 900)  # half-hour = 900s 15min有效期
    # 发送邮件
    authtype = 0
    send_mail(to=email, username=username, authcode=authcode, authtype=authtype)
    return jsonify({'message': '验证码发送成功'}), 200


@auth_bp.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    authcode_client = data.get('authcode')

    if not all([username, password, email, authcode_client]):
        return jsonify({'message': '请输入完整的注册信息'}), 400

    # user_name = User.query.filter_by(username=username).first()
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400

    # 从Redis中获取此邮箱对应的验证码, 与前端传来的数据校验
    try:
        authcode_server = redis_conn.get('AUTHCODE:' + email).decode()
    except Exception as e:
        print(e)
        return jsonify({'message': '查询邮箱验证码失败'}), 400
    if authcode_server != authcode_client:
        print('server: ', authcode_server, ', client: ', authcode_client)
        return jsonify({'message': '邮箱验证码错误'}), 400

    user = User()
    user.username = username
    user.email = email
    user.password = password
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功，请登录'}), 201


# 找回密码时发送邮箱验证码
@auth_bp.route('/authenticate/retrieve', methods=['POST'])
@cross_origin(supports_credentials=True)
def authenticate_retrieve():
    data = request.get_json()
    email = data.get('email')

    # 邮箱匹配正则
    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
        return jsonify({'message': '请填写正确的邮箱'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': '该邮箱还未注册'}), 400

    # 生成验证码
    authcode = '%06d' % random.randint(0, 99999)
    print('邮箱验证码为: ' + authcode)
    redis_conn.set('AUTHCODE:' + email, authcode, 900)  # half-hour = 900s 15min有效期
    # 发送邮件
    authtype = 1
    send_mail(to=email, username=user.username, authcode=authcode, authtype=authtype)
    return jsonify({'message': '验证码发送成功'}), 200


@auth_bp.route('/retrieve', methods=['POST'])
@cross_origin(supports_credentials=True)
def retrieve():
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')
    authcode_client = data.get('authcode')

    if not all([password, email, authcode_client]):
        return jsonify({'message': '请输入完整的注册信息'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': '该邮箱还未注册'}), 400

    # 从Redis中获取此邮箱对应的验证码, 与前端传来的数据校验
    try:
        authcode_server = redis_conn.get('AUTHCODE:' + email).decode()
    except Exception as e:
        print(e)
        return jsonify({'message': '查询邮箱验证码失败'}), 400
    if authcode_server != authcode_client:
        print('server: ', authcode_server, ', client: ', authcode_client)
        return jsonify({'message': '邮箱验证码错误'}), 400

    user.password = password
    db.session.commit()
    return jsonify({'message': '密码修改成功，请登录'}), 201


@auth_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if not user:
        user = User.query.filter_by(email=username).first()

    if user and user.verify_password(password):
        login_user(user)
        role = 'admin' if user.is_admin else 'user'
        current_user.setAllMessages([], [], [])
        db.session.commit()
        return jsonify({'message': '登录成功', 'role': role}), 200
    else:
        return jsonify({'message': '登录失败，请检查用户名/邮箱和密码'}), 401


@auth_bp.route('/logout', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': '登出成功'}), 200
