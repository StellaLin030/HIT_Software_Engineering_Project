from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from llm import llm_bp
from auth import auth_bp
from feedback import feedback_bp
from models import db, mail, User


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_pyfile('config.py')  # 从配置文件中加载配置

db.init_app(app)
mail.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(llm_bp, url_prefix='')
app.register_blueprint(auth_bp, url_prefix='')
app.register_blueprint(feedback_bp, url_prefix='')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000,threaded=True)
