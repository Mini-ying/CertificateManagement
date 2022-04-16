from flask import Blueprint, session, jsonify, g
from flask_restful import Api, reqparse, fields, marshal_with, inputs, Resource, marshal
from sqlalchemy import and_

from backend.tools.check_login import is_login
from backend.models import *
from backend.tools.response_code import RET

pro_bp=Blueprint('project',__name__)

api=Api(pro_bp)

project_fields={
    'project_id':fields.String,
    'project_name':fields.String,
}

#添加的传入
add_parser=reqparse.RequestParser()
add_parser.add_argument('project_id',type=str,required=True,help='必须填写project_id')
add_parser.add_argument('project_name',type=str,required=True,help='必须填写project_name',location='form')

#查询的传入
search_parser=reqparse.RequestParser()
search_parser.add_argument('type',type=str,required=True,help='必须选择查询类型',location='form')
search_parser.add_argument('info',type=str,required=True,help='必须填写查询信息',location='form')

#修改的传入
update_parser=add_parser.copy()

#删除的传入
delete_parser=reqparse.RequestParser()
delete_parser.add_argument('project_id',type=str,required=True,help='必须填写要删除的project_id')


class ProjectListApi(Resource):
    @is_login
    def get(self):   #显示当前项目列表
        user_id = g.user.user_id
        user = UserInfo.query.get(user_id)
        projects = user.projects

        return {'re_code':RET.OK, 'msg':'查询成功','projects':marshal(projects,project_fields)}


class ProjectApi(Resource):
    @is_login
    def get(self): #查询项目
        args = search_parser.parse_args()
        user_id = g.user.user_id
        type=args.get('type')
        info=args.get('info')

        if type=='project_id': #通过项目编号查询
            projects=Project.query.filter(and_(Project.project_id.contains(info),Project.project_id==User_projects.project_id,
                                               User_projects.user_id==user_id)).all()
            if projects:
                return {'re_code':RET.OK, 'msg':'查询成功', 'projects':marshal(projects,project_fields)}

            else:
                return jsonify(re_code=RET.NODATA,msg="项目不存在")

        if type=='project_name':  #通过项目名查询
            projects=Project.query.filter(and_(Project.project_name.like('%'+info+'%'),Project.project_id==User_projects.project_id,
                                               User_projects.user_id==user_id)
                                          ).all()
            if projects:
                return {'re_code':RET.OK, 'msg':'查询成功', 'projects':marshal(projects,project_fields)}

            else:
                return jsonify(re_code=RET.NODATA, msg="项目不存在")

    @is_login
    def post(self): #添加项目
        args = add_parser.parse_args()
        p_id=args.get('project_id')
        p_name = args.get('project_name')
        user_id = g.user.user_id

        p_i = Project.query.filter(Project.project_id == p_id).first()
        p_n = Project.query.filter(Project.project_name == p_name).first()

        # 判断要添加的信息是否存在
        if p_i:
            return jsonify(re_coder=RET.DATAEXIST, msg="项目id不能重复，请修改！")
        if p_n:
            return jsonify(re_coder=RET.DATAEXIST, msg="项目名不能重复，请修改！")

        # 保存新增项目信息
        user = UserInfo.query.filter_by(user_id=user_id).first()
        pj = Project(project_id=p_id, project_name=p_name)
        pj.users.append(user)

        db.session.add(pj)
        db.session.commit()

        projects = user.projects
        return {'re_code':RET.OK, 'msg':'添加成功', 'projects':marshal(projects,project_fields)}

    @is_login
    def patch(self): #编辑项目
        args=update_parser.parse_args()
        # 获取需要修改的项目
        p_id=args.get('project_id')
        p_name = args.get('project_name')
        user_id = g.user.user_id

        project = Project.query.filter(Project.project_id == p_id).first()
        p_n = Project.query.filter(Project.project_name == p_name).first()

        # 判断修改后的信息是否重复
        if p_n:
            return jsonify(re_coder=RET.DATAEXIST, msg="项目名不能重复，请修改！")

        # 保存修改后的项目信息
        project.project_name=p_name
        db.session.commit()

        user = UserInfo.query.get(user_id)
        projects = user.projects
        return {'re_code': RET.OK, 'msg': '编辑成功', 'projects': marshal(projects, project_fields)}

    @is_login
    def delete(self): #删除项目
        args=delete_parser.parse_args()
        pid = args.get('project_id')
        user_id = g.user.user_id
        project = Project.query.get(pid)
        user = UserInfo.query.get(user_id)

        #删除项目下的所有证书
        certificates=Certificate.query.filter(Certificate.project_id==pid).all()
        for certificate in certificates:
            db.session.delete(certificate)
            db.session.commit()

        #删除项目下的所有届次
        sessionns=Session.query.filter(Session.project_id==pid).all()
        for sessionn in sessionns:
            user.sessions.remove(sessionn)
            db.session.delete(sessionn)
            db.session.commit()

        #解除项目和用户的关系
        user.projects.remove(project)
        db.session.delete(project)
        db.session.commit()

        projects = user.projects
        return {'re_code': RET.OK, 'msg': '删除成功', 'projects': marshal(projects, project_fields)}


api.add_resource(ProjectListApi, '/projectList')
api.add_resource(ProjectApi, '/project')
