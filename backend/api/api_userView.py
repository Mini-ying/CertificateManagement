import random
import uuid

from flask import Blueprint, session, jsonify, g
from flask_restful import Api, reqparse, fields, marshal_with, inputs, Resource, marshal
from werkzeug.security import check_password_hash, generate_password_hash

from backend.app_config import cache
from backend.tools.check_login import is_login
from backend.models import UserInfo,db
from backend.tools.response_code import RET

user_bp=Blueprint('user',__name__)

api=Api(user_bp)

user_fields={
    'user_id':fields.String,
    'username':fields.String,
    'phone':fields.String
}

#参数解析
parser=reqparse.RequestParser()

#登录的传入
parser.add_argument('user_id',type=inputs.regex(r'^[0-9]*$'),required=True,help='账号有非法字符',location=['form'])
parser.add_argument('password',type=str,required=True,help='密码不能为空',location=['form'])

#修改用户信息的传入
edit_parser=reqparse.RequestParser()
edit_parser.add_argument('password',type=str,location='form')
edit_parser.add_argument('repassword',type=str,location='form')
edit_parser.add_argument('username',type=str,location='form')
edit_parser.add_argument('phone',type=str,location='form')

class UserLogin(Resource):
    def post(self):
        args=parser.parse_args()
        user_id=args.get('user_id')
        password=args.get('password')

        # 判断用户名和密码的是否填写
        if not user_id:
            return jsonify(re_code=RET.PARAMERR, msg="用户账号未填写")
        if not password:
            return jsonify(re_code=RET.PARAMERR, msg="密码未填写")

        user = UserInfo.query.filter_by(user_id=user_id, password=password).first()
        # 如果检查密码一致,则登录成功
        if user:
            #生成令牌
            token=str(uuid.uuid4()).replace('-','')+str(random.randint(100,999))
            #存储用户的信息
            cache.set(token, user.user_id,timeout=60*60*24)
            #向session写入数据
            # session['user_id'] = user.user_id
            # session['token']=token
            # print(session.get(token))
            return {'re_code':RET.OK, 'msg':'登录成功', 'user':marshal(user,user_fields),'token':token}
        else:
            # 用户名或密码不正确
            return jsonify(re_code=RET.DATAERR, msg="账号或密码错误")


class UserLogout(Resource):
    def delete(self):
        """
            退出登录
            """
        # 清空session
        session.clear()
        return jsonify(re_code=RET.OK, msg="已退出登录")

#用户个人中心
class UserCenter(Resource):
    # 显示用户个人中心主页
    @is_login
    def get(self):
        user_id = g.user.user_id
        user=UserInfo.query.filter(UserInfo.user_id==user_id).first()
        return {'re_code':RET.OK, 'msg':'成功进入用户个人中心', 'user':marshal(user,user_fields)}

    # 用户修改个人信息
    @is_login
    def put(self):
        args=edit_parser.parse_args()
        username=args.get('username')
        password=args.get('password')
        repassword=args.get('repassword')
        phone=args.get('phone')

        user_id=g.user.user_id
        user = UserInfo.query.filter(UserInfo.user_id == user_id).first()

        #若修改用户名
        if username:
            # 验证是否有重名用户
            name = UserInfo.query.filter(UserInfo.username == username).first()
            if name:
                return jsonify(re_code=RET.DATAEXIST, msg="该用户名已被注册,请修改！")
            else:
                user.username = username

        #若修改手机
        if phone:
            #验证手机号是否唯一
            user_phone=UserInfo.query.filter(UserInfo.phone==phone).first()
            if user_phone:
                return jsonify(re_code=RET.DATAEXIST, msg="该手机号已被注册,请修改！")
            else:
                user.phone = phone

        #若修改密码
        if repassword:
            #若两次输入密码一致
            if password == repassword:
                user.password = password
                db.session.commit()
                return {'re_code': RET.OK, 'msg': '修改密码成功'}
            else:
                return {'re_code': RET.PWDERR, 'msg': '两次密码不一致！'}

        db.session.commit()
        user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
        return {'re_code': RET.OK, 'msg': '修改个人信息成功','user':marshal(user,user_fields)}


api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')
api.add_resource(UserCenter,'/User')