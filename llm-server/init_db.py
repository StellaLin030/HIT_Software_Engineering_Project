from app import app
from models import User, Feedback, Conversations, db

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.password = 'admin'
        db.session.add(admin)
        db.session.commit()
        print("管理员用户已创建")
    else:
        print("管理员用户已存在")
