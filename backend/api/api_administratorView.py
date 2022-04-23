from flask import Blueprint, session, jsonify, g
from flask_restful import Api, reqparse, fields, marshal_with, inputs, Resource, marshal
from sqlalchemy import and_

from backend.tools.check_login import is_admin
from backend.models import *
from backend.tools.response_code import RET

admin_bp=Blueprint('admin',__name__)

api=Api(admin_bp)

user_fields={
    'user_id':fields.String,
    'username':fields.String,
    'password':fields.String,
    'phone':fields.String,
    'role':fields.String
}

#查找用户的传入
search_parser=reqparse.RequestParser()
search_parser.add_argument('type',type=str,required=True,help='必须选择查询类型',location=['form','args'])
search_parser.add_argument('info',type=str,required=True,help='必须填写查询信息',location=['form','args'])

#添加用户的传入
add_parser=reqparse.RequestParser()
add_parser.add_argument('user_id',type=str,required=True,help='必须填写user_id',location='form')
add_parser.add_argument('username',type=str,required=True,help='必须填写username',location='form')
add_parser.add_argument('phone',type=str,location='form')
add_parser.add_argument('role',type=str,required=True,help='必须填写用户权限role',location='form')

#删除用户的传入
del_parser=reqparse.RequestParser()
del_parser.add_argument('user_id',type=str,required=True,help='必须传入要删除的user_id',location=['form','args'])

# 查看当前系统已注册的用户
class UserList(Resource):
    @is_admin
    def get(self):
        users = UserInfo.query.all()
        return {'re_code': RET.OK, 'msg': '查询用户成功', 'users': marshal(users, user_fields)}


#管理员后台管理页面
class AdminCenter(Resource):
    # 查找用户
    @is_admin
    def get(self):
        args = search_parser.parse_args()
        type = args.get('type')
        info = args.get('info')

        #根据用户名搜索
        if type=='username':
            users=UserInfo.query.filter(UserInfo.username.like('%'+info+'%')).all()
            if users:
                return {'re_code': RET.OK, 'msg': '查询成功', 'users': marshal(users, user_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="用户不存在")


        #根据用户账号搜索
        if type=='user_id':
            users=UserInfo.query.filter(UserInfo.user_id.like('%'+info+'%')).all()
            if users:
                return {'re_code': RET.OK, 'msg': '查询成功', 'users': marshal(users, user_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="用户不存在")

        #根据手机号搜索
        if type=='phone':
            users=UserInfo.query.filter(UserInfo.phone.like('%'+info+'%')).all()
            if users:
                return {'re_code': RET.OK, 'msg': '查询成功', 'users': marshal(users, user_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="用户不存在")

        # 根据手机号搜索
        if type == 'role':
            users = UserInfo.query.filter(UserInfo.role.like('%' + info + '%')).all()
            if users:
                return {'re_code': RET.OK, 'msg': '查询成功', 'users': marshal(users, user_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="用户不存在")


    #添加用户
    @is_admin
    def post(self):
        args = add_parser.parse_args()
        user_id=args.get('user_id')
        username=args.get('username')
        phone = args.get('phone') #手机不是必填项
        role = args.get('role')

        #验证用户账号是否唯一
        check_id=UserInfo.query.filter(UserInfo.user_id==user_id).first()
        if check_id:
            return jsonify(re_coder=RET.DATAEXIST, msg="用户id不能重复，请修改！")

        #验证用户名是否唯一
        check_name=UserInfo.query.filter(UserInfo.username==username).first()
        if check_name:
            return jsonify(re_coder=RET.DATAEXIST, msg="用户名不能重复，请修改！")

        #验证用户手机号是否唯一
        if phone:
            check_phone = UserInfo.query.filter(UserInfo.phone == phone).first()
            if check_phone:
                return jsonify(re_coder=RET.DATAEXIST, msg="用户手机号不能重复，请修改！")

        #新用户默认密码为123456
        password='123456'

        #保存新增用户信息
        user=UserInfo(user_id=user_id,username=username,phone=phone,role=role,password=password)
        db.session.add(user)
        db.session.commit()

        users = UserInfo.query.all()
        return {'re_code': RET.OK, 'msg': '添加用户成功', 'users': marshal(users, user_fields)}

    #删除用户
    @is_admin
    def delete(self):
        args = del_parser.parse_args()
        user_id = args.get('user_id')
        user=UserInfo.query.get(user_id)

        # 删除该用户的证书信息
        certificates = Certificate.query.filter(Certificate.user_id == user_id).all()
        for certificate in certificates:
            db.session.delete(certificate)

        # 删除该用户的届次信息
        sessionns = Session.query.filter(
            and_(Session.session_id == User_sessions.session_id, User_sessions.user_id == user_id)).all()
        for sessionn in sessionns:
            sessionn.users.remove(user)
            db.session.delete(sessionn)

        #删除该用户的项目信息
        projects=Project.query.filter(and_(Project.project_id==User_projects.project_id,User_projects.user_id==user_id)).all()
        for project in projects:
            project.users.remove(user)
            db.session.delete(project)

        db.session.delete(user)
        db.session.commit()
        users = UserInfo.query.all()
        return {'re_code': RET.OK, 'msg': '删除用户成功', 'users': marshal(users, user_fields)}


api.add_resource(AdminCenter,'/Admin')
api.add_resource(UserList,'/UserList')