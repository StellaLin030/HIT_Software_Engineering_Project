from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import User, Feedback, db
from flask_cors import cross_origin
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

feedback_bp = Blueprint('feedback', __name__)


@feedback_bp.route('/user/feedback', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_required
def user_feedback():
    data = request.get_json()
    message = data.get('message')
    if message:
        feedback = Feedback(user_id=current_user.id, message=message)
        db.session.add(feedback)
        db.session.commit()
        return jsonify({'message': '反馈已提交'}), 200
    else:
        return jsonify({'error': '未提供反馈信息'}), 400


# 获取所有反馈信息,但不会标记未读的为已读的！！！
@feedback_bp.route('/admin/feedback')
@cross_origin(supports_credentials=True)
@login_required
def admin_feedback():
    if not current_user.is_admin:
        return jsonify({'error': '您没有权限查看'}), 403

    feedbacks = Feedback.query.all()
    formatted_feedbacks = [
        {'id': feedback.id,
         'user_id': feedback.user_id,
         'username': feedback.user.username,
         'message': feedback.message,
         'timestamp': feedback.timestamp}
        for feedback in feedbacks]

    return jsonify({'feedbacks': formatted_feedbacks}), 200


@feedback_bp.route('/admin/users', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def admin_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    users = User.query.all()
    user_list = [{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'create_time': user.created_at,
    } for user in users]

    return jsonify({'users': user_list}), 200


# 获取用户总人数
@feedback_bp.route('/admin/number_user', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def admin_total_user():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    user_count = User.query.count()
    return jsonify({'total_users': user_count})


# 获取增长人数(较上月)
@feedback_bp.route('/admin/increase_user', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def admin_increase_user():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    '''
    #这样获得的当前时间为结束时间的一个月内的人数
    # 获取当前时间和上个月的时间
    now = datetime.utcnow()
    # 精确获得上个月
    last_month = now - relativedelta(months=1)
    print(now)
    print(last_month)
    # 查询上个月的用户增长数
    increase_count = User.query.filter(User.created_at >= last_month).count()

    return jsonify({'increase_users': increase_count})
    '''
    # 这样获得的是当前时间所在月份从1号开始到现在增长人数
    # 获取当前时间
    now = datetime.utcnow()

    # 获取当月1日的时间，重置时分秒为零
    first_day_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # print(now)
    # print(first_day_of_current_month)

    # 查询当月1日以来的用户增长数
    increase_count = User.query.filter(User.created_at >= first_day_of_current_month).count()
    return jsonify({'increase_users': increase_count})


# 获取未读反馈总数
@feedback_bp.route('/admin/number_unreadfeedback', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def number_unreadfeedback():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    unread_feedback_count = Feedback.query.filter_by(is_read=False).count()
    return jsonify({'unread_feedback': unread_feedback_count})


# 获取所有未读反馈信息
@feedback_bp.route('/admin/unreadfeedback')
@cross_origin(supports_credentials=True)
@login_required
def admin_unreadfeedback():
    if not current_user.is_admin:
        return jsonify({'error': '您没有权限查看'}), 403

    feedbacks = Feedback.query.filter_by(is_read=False)
    formatted_feedbacks = [
        {'id': feedback.id,
         'user_id': feedback.user_id,
         'username': feedback.user.username,
         'message': feedback.message,
         'timestamp': feedback.timestamp}
        for feedback in feedbacks]

    # 将未读反馈信息状态修改为已读
    for feedback in feedbacks:
        feedback.is_read = True

    # 提交更改到数据库
    db.session.commit()

    return jsonify({'feedbacks': formatted_feedbacks}), 200


# 获取总反馈数 /admin/number_allfeedback
@feedback_bp.route('/admin/number_allfeedback', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def number_allfeedback():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    all_feedback_count = Feedback.query.count()
    return jsonify({'allfeedback': all_feedback_count})


# 获取当月新增用户信息
@feedback_bp.route('/admin/crease_users', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def admin_crease_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        # 获取当前时间
    now = datetime.utcnow()

    # 获取当月1日的时间，重置时分秒为零
    first_day_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 查询当月1日以来的用户
    users = User.query.filter(User.created_at >= first_day_of_current_month)
    user_list = [{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'create_time': user.created_at,
    } for user in users]
    return jsonify({'users': user_list}), 200