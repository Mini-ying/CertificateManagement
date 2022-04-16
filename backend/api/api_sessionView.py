from flask import Blueprint, session, jsonify, g
from flask_restful import Api, reqparse, fields, marshal_with, inputs, Resource, marshal
from sqlalchemy import and_

from backend.tools.check_login import is_login
from backend.models import *
from backend.tools.response_code import RET

ses_bp=Blueprint('session',__name__)

api=Api(ses_bp)

session_fields={
    'session_id':fields.String,
    'number':fields.String,
    'category':fields.String,
}

#显示届次的传入
parser=reqparse.RequestParser()
parser.add_argument('project_id',type=str,required=True,help='必须传入项目id',location='form')

#查询的传入
search_parser=parser.copy()
search_parser.add_argument('type',type=str,required=True,help='必须选择查询类型',location='form')
search_parser.add_argument('info',type=str,required=True,help='必须填写查询信息',location='form')

#添加的传入
add_parser=parser.copy()
add_parser.add_argument('session_id',type=str,required=True,help='必须填写届次号',location='form')
add_parser.add_argument('number',type=str,required=True,help='必须填写第几届',location='form')
add_parser.add_argument('category',type=str,required=True,help='必须填写届次类别',location='form')


#修改的传入
update_parser=add_parser.copy()

#删除的传入
delete_parser=parser.copy()
delete_parser.add_argument('session_id',type=str,required=True,help='必须传入要删除的届次号')


class SessionListApi(Resource):
    @is_login
    def get(self):   #显示当前项目下的届次列表
        args=parser.parse_args()
        project_id = args.get('project_id')
        user_id = g.user.user_id
        sessions=Session.query.filter(and_(Session.project_id==project_id,User_sessions.user_id==user_id,User_sessions.session_id==Session.session_id
                                               )).all()
        if sessions:
            return {'re_code': RET.OK, 'msg': '查询成功', 'sessions': marshal(sessions, session_fields)}
        else:
            return {'msg':'当前项目暂无届次信息'}


class SessionApi(Resource):
    @is_login
    def get(self): #查询届次
        args = search_parser.parse_args()
        user_id = g.user.user_id
        project_id=args.get('project_id')
        type=args.get('type')
        info=args.get('info')

        if type=='number': #通过届次来查询
            sessions=Session.query.filter(and_(Session.number.like('%'+info+'%'),Session.project_id==project_id,
                                               User_sessions.session_id==Session.session_id,
                                               User_sessions.user_id==user_id)).all()
            if sessions:
                return {'re_code':RET.OK, 'msg':'查询成功', 'sessions':marshal(sessions,session_fields)}
            else:
                return jsonify(re_code=RET.NODATA,msg="不存在该届次")

        if type=='category':  #通过届次类别查询
            sessions = Session.query.filter(and_(Session.category.like('%'+info+'%'),Session.project_id == project_id,
                                                 User_sessions.session_id == Session.session_id,
                                                 User_sessions.user_id == user_id)).all()

            if sessions:
                return {'re_code':RET.OK, 'msg':'查询成功', 'sessions':marshal(sessions,session_fields)}

            else:
                return jsonify(re_code=RET.NODATA, msg="不存在该届次")

    @is_login
    def post(self): #添加届次
        args = add_parser.parse_args()
        project_id=args.get('project_id')
        user_id = g.user.user_id
        session_id = args.get('session_id')
        number=args.get('number')
        category=args.get('category')

        #判断该用户是否存在该项目
        projects = Project.query.filter(
            and_(Project.project_id.contains(project_id), Project.project_id == User_projects.project_id,
                 User_projects.user_id == user_id)).all()

        if not projects:
            return jsonify(re_coder=RET.NODATA, msg="不存在该项目，请先添加项目！")

        #验证届次号是否唯一
        s=Session.query.filter(Session.session_id==session_id).first()
        if s:
            return jsonify(re_coder=RET.DATAEXIST, msg="届次号不能重复，请修改！")

        # 判断要添加的信息是否存在
        sessionn = Session.query.filter(and_(Session.number == number,
                                            Session.category == category,
                                             Session.project_id == project_id,
                                             User_sessions.session_id == session_id,
                                             User_sessions.user_id == user_id)).first()

        if sessionn:
            return jsonify(re_coder=RET.DATAEXIST, msg="该届次已存在，请修改！")

        # 保存新增项目信息
        user = UserInfo.query.filter_by(user_id=user_id).first()
        ses=Session(session_id=session_id,number=number,category=category,project_id=project_id)
        ses.users.append(user)

        db.session.add(ses)
        db.session.commit()

        sessions = Session.query.filter(
            and_(Session.project_id == project_id, User_sessions.session_id == Session.session_id,
                 User_sessions.user_id == user_id)).all()

        return {'re_code':RET.OK, 'msg':'添加成功', 'sessions':marshal(sessions,session_fields)}

    @is_login
    def patch(self): #编辑项目
        args=update_parser.parse_args()
        # 获取需要修改的项目
        user_id = g.user.user_id
        project_id = args.get('project_id')
        session_id = args.get('session_id')
        number = args.get('number')
        category = args.get('category')

        # 判断修改后的信息是否存在完全一致的
        sessionn = Session.query.filter(and_(Session.number == number,Session.category == category,Session.project_id == project_id,
                                             User_sessions.session_id == Session.session_id,User_sessions.user_id == user_id)).first()

        if sessionn:
            return jsonify(re_coder=RET.DATAEXIST, msg="该届次已存在，请修改！")

        # 保存修改后的项目信息
        user = UserInfo.query.get(user_id)
        ses=Session.query.get(session_id)

        ses.number=number
        ses.category=category
        db.session.commit()

        sessions = Session.query.filter(
            and_(Session.project_id == project_id, User_sessions.session_id == Session.session_id,
                 User_sessions.user_id == user_id)).all()
        return {'re_code': RET.OK, 'msg': '编辑成功', 'sessions': marshal(sessions, session_fields)}

    @is_login
    def delete(self): #删除届次
        args=delete_parser.parse_args()
        session_id = args.get('session_id')
        user_id = g.user.user_id
        project_id=args.get('project_id')

        #删除该届次下的所有证书
        certificates=Certificate.query.filter(Certificate.session_id==session_id).all()
        for certificate in certificates:
            db.session.delete(certificate)
            db.session.commit()

        #解除届次和用户的关联关系
        sessionn=Session.query.get(session_id)
        user = UserInfo.query.get(user_id)
        user.sessions.remove(sessionn)

        db.session.delete(sessionn)
        db.session.commit()

        sessionns = Session.query.filter(and_(Session.project_id == project_id,
                                            User_sessions.user_id == user_id)).all()
        return {'re_code': RET.OK, 'msg': '删除成功', 'sessions': marshal(sessionns, session_fields)}


api.add_resource(SessionListApi, '/sessionList')
api.add_resource(SessionApi, '/session')
