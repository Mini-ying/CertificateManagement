from flask import  session, jsonify, g, request
from functools import wraps
from flask_restful import abort

from backend.app_config import cache
from backend.models import UserInfo


#验证令牌
def check_user():
    auth=request.headers.get('Authorization')
    if not auth:
        abort(401,msg='请先登录')
    user_id=cache.get(auth)
    print(user_id)
    if not user_id:
        abort(401,msg='无效令牌')
    user=UserInfo.query.filter(UserInfo.user_id==user_id).first()
    if not user:
        abort(401,msg='此用户已被管理员删除')
    g.user=user


def is_login(func):
    """登录校验装饰器
     :param func:函数名
     :return: 闭包函数名
     """

    # 装饰器装饰一个函数时，会修改该函数的__name__属性
    # 如果希望装饰器装饰之后的函数，依然保留原始的名字和说明文档,就需要使用wraps装饰器，装饰内存函数
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_user()
        return func(*args, **kwargs)
    return wrapper


def is_admin(func):
    #验证管理员身份装饰器
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_user()
        if g.user.role=='administrator':
            return func(*args, **kwargs)
        abort(401, msg='非管理员禁止进入')
    return wrapper