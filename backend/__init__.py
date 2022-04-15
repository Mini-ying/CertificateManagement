from flask import Flask
from flask_cors import CORS

from backend.api.api_administratorView import admin_bp
from backend.api.api_cetificateView import certifi_bp
from backend.api.api_projectView import pro_bp
from backend.api.api_sessionView import ses_bp
from backend.api.api_userView import user_bp
from backend.app_config import db, cache
import backend.app_config

config={
    'CACHE_TYPE':'redis',
    'CACHE_REDIS_HOST':'127.0.0.1',
    'CACHE_REDIS_PORT':6379
}


def create_app():
    app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
    app.config.from_object(app_config.Config)

    db.init_app(app=app)

    #跨域
    CORS(app, supports_credentials=True)

    #初始化缓存文件
    cache.init_app(app=app, config=config)

    #注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(pro_bp)
    app.register_blueprint(ses_bp)
    app.register_blueprint(certifi_bp)
    app.register_blueprint(admin_bp)

    return app











