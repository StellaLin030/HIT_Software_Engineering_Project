SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 添加邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = 'True'
MAIL_PORT = '465'
MAIL_USERNAME = '1668169699@qq.com'  # 发送邮箱账号
MAIL_PASSWORD = 'aoivdtanjgkfeihe'  # 授权码
MAIL_DEFAULT_SENDER = '1668169699@qq.com'  # 验证码默认发送邮箱
FLASK_MAIL_SUBJECT_PREFIX = '[ChatWithAIs AuthCode]'     # 邮件标题
FLASK_MAIL_SENDER = 'HIT ChatWithAIs team <1668169699@qq.com>'   # 邮件发送方
# Redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1