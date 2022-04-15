from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# 注册数据模型
db = SQLAlchemy()

cache=Cache()


class Config:
    DEBUG=True

    # 配置数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:384845100@127.0.0.1:3306/certificationmanagement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True

    # 设置session密钥
    SECRET_KEY = 'd890fbe7e26c4c3eb557b6009e3f4d3d'

    # 设置连接的redis数据库 默认连接到本地6379
    SESSION_TYPE = 'redis'


# # 设置远程
# app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)



