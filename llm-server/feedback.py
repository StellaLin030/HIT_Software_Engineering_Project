from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import User, Feedback, db
from flask_cors import cross_origin

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
    } for user in users]

    return jsonify({'users': user_list}), 200
