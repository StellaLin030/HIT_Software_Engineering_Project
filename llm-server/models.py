from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # tln新增
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # xqq新增 4个字段
    conversation_current_id = db.Column(db.Integer, default=0)
    current_chatgpt_messages = db.Column(db.JSON, default='[]')
    current_wenxin_messages = db.Column(db.JSON, default='[]')
    current_tongyi_messages = db.Column(db.JSON, default='[]')

    @property
    def password(self):
        raise AttributeError('密码不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('feedback', lazy=True))
    # 新增 为了显示未读反馈信息
    is_read = db.Column(db.Boolean, default=False, nullable=False)


class Conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chatgpt_messages = db.Column(db.JSON)  # 改为 JSON 类型
    wenxin_messages = db.Column(db.JSON)   # 改为 JSON 类型
    tongyi_messages = db.Column(db.JSON)   # 改为 JSON 类型
    summary = db.Column(db.String(15))       # 来自文心一言的总结
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
