SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 添加邮箱配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '25'
MAIL_USE_TLS = True
MAIL_USERNAME = 'hitchatwithaisteam@163.com'
MAIL_PASSWORD = 'PYBYOUUZHDICZMRN'
MAIL_DEFAULT_SENDER = 'hitchatwithaisteam@163.com'
FLASK_MAIL_SUBJECT_PREFIX = '[ChatWithAIs AuthCode]'
FLASK_MAIL_SENDER = 'HIT ChatWithAIs team <hitchatwithaisteam@163.com>'
# Redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1