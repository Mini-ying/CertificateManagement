import xlrd
from flask import Blueprint, session, jsonify, g
from flask_restful import Api, reqparse, fields, marshal_with, inputs, Resource, marshal
from sqlalchemy import and_
from werkzeug.datastructures import FileStorage

from backend.tools.check_login import is_login
from backend.models import *
from backend.tools.response_code import RET
from backend.tools.changeDatetime import CustomDate

certifi_bp=Blueprint('certificate',__name__)

api=Api(certifi_bp)

certificate_fields={
    'certificate_id':fields.String,
    'certificate_name':fields.String,
    'level':fields.String,
    'winner':fields.String,
    'rank': fields.String,
    'date':CustomDate(dt_format='strftime'),
    'giver':fields.String
}

#直接进入证书管理页面的fields
Allcertificate_fields={
    'project_id':fields.String,
    'session_id':fields.String,
    'certificate_id':fields.String,
    'certificate_name':fields.String,
    'level':fields.String,
    'winner':fields.String,
    'rank': fields.String,
    'date':CustomDate(dt_format='strftime'),
    'giver':fields.String
}

#显示项目的传入
parser=reqparse.RequestParser()
parser.add_argument('project_id',type=str,required=True,help='必须传入项目id',location=['form','args'])
parser.add_argument('session_id',type=str,required=True,help='必须传入届次id',location=['form','args'])

#查询的传入
search_parser=parser.copy()
search_parser.add_argument('type',type=str,required=True,help='必须选择查询类型',location=['form','args'])
search_parser.add_argument('info',type=str,required=True,help='必须填写查询信息',location=['form','args'])

#添加的传入
add_parser=parser.copy()
add_parser.add_argument('certificate_id',type=str,location='form')
add_parser.add_argument('certificate_name',type=str,location='form')
add_parser.add_argument('winner',type=str,location='form')
add_parser.add_argument('level',type=str,location='form')
add_parser.add_argument('rank',type=str,location='form')
add_parser.add_argument('date',type=str,location='form')
add_parser.add_argument('giver',type=str,location='form')

#修改的传入
update_parser=add_parser.copy()

#删除的传入
delete_parser=parser.copy()
delete_parser.add_argument('certificate_id',type=str,required=True,help='必须填写要删除的certificate_id',location=['form','args'])

#导出单个证书的传入
ex_single_parser=parser.copy()
ex_single_parser.add_argument('certificate_id',type=str,required=True,help='必须传入要导出的certificate_id')

#批量导入证书的传入
im_parser=reqparse.RequestParser()
im_parser.add_argument('file',type=FileStorage,location='files',required=True,help='必须上传文件')

#直接进入证书页面的传入
#查询
Allsearch_parser=reqparse.RequestParser()
Allsearch_parser.add_argument('type',type=str,required=True,help='必须选择查询类型',location=['form','args'])
Allsearch_parser.add_argument('info',type=str,required=True,help='必须填写查询信息',location=['form','args'])

#添加使用上面的传入

#编辑
Allupdate_parser=reqparse.RequestParser()
Allupdate_parser.add_argument('certificate_id',type=str,location='form')
Allupdate_parser.add_argument('certificate_name',type=str,location='form')
Allupdate_parser.add_argument('winner',type=str,location='form')
Allupdate_parser.add_argument('level',type=str,location='form')
Allupdate_parser.add_argument('rank',type=str,location='form')
Allupdate_parser.add_argument('date',type=str,location='form')
Allupdate_parser.add_argument('giver',type=str,location='form')

#删除
Alldel_parser=reqparse.RequestParser()
Alldel_parser.add_argument('certificate_id',type=str,required=True,help='必须填写要删除的certificate_id',location=['form','args'])


class CertificateListApi(Resource):
    @is_login
    def get(self):   #显示当前证书列表
        args=parser.parse_args()
        user_id = g.user.user_id
        session_id = args.get('session_id')
        project_id = args.get('project_id')
        certificates = Certificate.query.filter(and_(Certificate.user_id == user_id,Certificate.session_id==session_id,Certificate.project_id==project_id)
                                                ).all()

        return {'re_code':RET.OK, 'msg':'显示成功','certificates':marshal(certificates,certificate_fields)}


#直接进入证书页面的接口
class AllCertificateListApi(Resource):
    @is_login
    def get(self):
        user_id = g.user.user_id
        certificates = Certificate.query.filter(Certificate.user_id == user_id).all()

        return {'re_code': RET.OK, 'msg': '显示成功', 'certificates': marshal(certificates, Allcertificate_fields)}


class CertificateApi(Resource):
    @is_login
    def get(self): #查询证书
        args = search_parser.parse_args()
        user_id = g.user.user_id
        type=args.get('type')
        info=args.get('info')
        project_id=args.get('project_id')
        session_id = args.get('session_id')

        if type == 'certificate_id':  # 通过证书编号查询
            certificates = Certificate.query.filter(and_(
                Certificate.certificate_id.like('%' + info + '%'), Certificate.user_id == user_id,
                Certificate.project_id==project_id,Certificate.session_id==session_id)).all()

            if certificates:
                return {'re_code':RET.OK, 'msg':'搜索成功','certificates':marshal(certificates,certificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type == 'certificate_name':  # 通过证书名查询
            certificates = Certificate.query.filter(and_(
                Certificate.certificate_name.like('%' + info + '%'), Certificate.user_id == user_id,
                Certificate.project_id==project_id,Certificate.session_id==session_id
            )).all()

            if certificates:
                return {'re_code':RET.OK, 'msg':'搜索成功','certificates':marshal(certificates,certificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type == 'winner':  # 通过获奖者查询
            certificates = Certificate.query.filter(and_(
                Certificate.winner.like('%' + info + '%'), Certificate.user_id == user_id,
                Certificate.project_id==project_id,Certificate.session_id==session_id)).all()
            if certificates:
                return {'re_code':RET.OK, 'msg':'搜索成功','certificates':marshal(certificates,certificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

    @is_login
    def post(self): #添加证书
        user_id = g.user.user_id
        
        args = add_parser.parse_args()
        p_id=args.get('project_id')
        session_id=args.get('session_id')
        c_id = args.get('certificate_id')

        #验证新增证书的项目是否存在
        pro = Project.query.filter(
            and_(Project.project_id == p_id, Project.project_id == User_projects.project_id,
                 User_projects.user_id == user_id)).all()
        if not pro:
            return jsonify(re_coder=RET.NODATA, msg="不存在该项目，请先添加项目！")

        #验证新增证书的届次是否存在
        sessions = Session.query.filter(and_(Session.session_id==session_id,Session.project_id == p_id,
                                             User_sessions.session_id == Session.session_id,
                                             User_sessions.user_id == user_id)).all()
        if not sessions:
            return jsonify(re_code=RET.DBERR, msg="该届次不存在，请先添加新届次！")


        #验证证书号是否唯一
        c_i = Certificate.query.filter(Certificate.certificate_id == c_id).first()
        if c_i:
            return jsonify(re_code=RET.DATAEXIST, msg="证书编号不能重复，请修改！")

        c_name = args.get('certificate_name')
        winner = args.get('winner')
        level = args.get('level')
        date = args.get('date')
        rank = args.get('rank')
        giver = args.get('giver')

        # 保存新增证书信息
        certificate = Certificate(certificate_id=c_id, certificate_name=c_name,  winner=winner,
                                  level=level, date=date, rank=rank, giver=giver, user_id=user_id,
                                  project_id=p_id,session_id=session_id)
        db.session.add(certificate)
        db.session.commit()

        certificates = Certificate.query.filter(
            and_(Certificate.user_id == user_id, Certificate.session_id == session_id,
                 Certificate.project_id == p_id)
            ).all()
        return {'re_code': RET.OK, 'msg': '添加成功', 'certificates': marshal(certificates,certificate_fields)}

    @is_login
    def put(self): #编辑证书
        user_id = g.user.user_id
        args=update_parser.parse_args()
        project_id = args.get('project_id')
        session_id = args.get('session_id')
        c_id = args.get('certificate_id')
        c_name = args.get('certificate_name')
        winner = args.get('winner')
        level = args.get('level')
        date = args.get('date')
        rank = args.get('rank')
        giver = args.get('giver')

        # 验证有无完全一致的证书
        certifi=Certificate.query.filter(and_(
            Certificate.certificate_name==c_name,Certificate.winner==winner,Certificate.level==level,Certificate.date==date,Certificate.rank==rank,Certificate.giver==giver)).first()
        if certifi:
            return jsonify(re_coder=RET.DATAEXIST, msg="该证书已存在，请修改！")
            
        # 获取需要修改的证书
        certificate=Certificate.query.get(c_id)

        # 修改并保存编辑后的证书
        certificate.certificate_name = c_name
        certificate.certificate_id = c_id
        certificate.winner = winner
        certificate.level = level
        certificate.date = date
        certificate.rank = rank
        certificate.giver = giver

        db.session.commit()

        certificates = Certificate.query.filter(
            and_(Certificate.user_id == user_id, Certificate.session_id == session_id,
                 Certificate.project_id == project_id)
        ).all()
        return {'re_code': RET.OK, 'msg': '修改成功', 'certificates': marshal(certificates, certificate_fields)}

    @is_login
    def delete(self): #删除证书
        user_id = g.user.user_id
        args=delete_parser.parse_args()
        pid = args.get('project_id')
        cid = args.get('certificate_id')
        session_id=args.get('session_id')

        # 获取需要删除的项目
        certificate = Certificate.query.filter(
            and_(Certificate.certificate_id == cid, Certificate.user_id == user_id,
                 Certificate.project_id == pid, Certificate.session_id == session_id)).first()

        db.session.delete(certificate)
        db.session.commit()

        certificates = Certificate.query.filter(
            and_(Certificate.user_id == user_id, Certificate.session_id == session_id,
                 Certificate.project_id == pid)
        ).all()
        return {'re_code': RET.OK, 'msg': '删除成功', 'certificates': marshal(certificates, certificate_fields)}


#直接进入证书管理页面的接口
class AllCertificateApi(Resource):
    @is_login
    def get(self):  # 查询证书
        args = Allsearch_parser.parse_args()
        user_id = g.user.user_id
        type = args.get('type')
        info = args.get('info')

        if type == 'certificate_id':  # 通过证书编号查询
            certificates = Certificate.query.filter(and_(
                Certificate.certificate_id.like('%' + info + '%'), Certificate.user_id == user_id)).all()

            if certificates:
                return {'re_code': RET.OK, 'msg': '搜索成功', 'certificates': marshal(certificates, Allcertificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type == 'certificate_name':  # 通过证书名查询
            certificates = Certificate.query.filter(and_(
                Certificate.certificate_name.like('%' + info + '%'), Certificate.user_id == user_id)).all()

            if certificates:
                return {'re_code': RET.OK, 'msg': '搜索成功', 'certificates': marshal(certificates, Allcertificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type == 'winner':  # 通过获奖者查询
            certificates = Certificate.query.filter(and_(
                Certificate.winner.like('%' + info + '%'), Certificate.user_id == user_id)).all()
            if certificates:
                return {'re_code': RET.OK, 'msg': '搜索成功', 'certificates': marshal(certificates, Allcertificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type=="project_id": #通过项目号查询
            certificates = Certificate.query.filter(and_(
                Certificate.project_id.like('%' + info + '%'), Certificate.user_id == user_id)).all()
            if certificates:
                return {'re_code': RET.OK, 'msg': '搜索成功', 'certificates': marshal(certificates, Allcertificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

        if type=="session_id": #通过届次号查询
            certificates = Certificate.query.filter(and_(
                Certificate.session_id.like('%' + info + '%'), Certificate.user_id == user_id)).all()
            if certificates:
                return {'re_code': RET.OK, 'msg': '搜索成功', 'certificates': marshal(certificates, Allcertificate_fields)}
            else:
                return jsonify(re_code=RET.NODATA, msg="证书不存在")

    @is_login
    def post(self):  # 添加证书
        user_id = g.user.user_id

        args = add_parser.parse_args()
        p_id = args.get('project_id')
        session_id = args.get('session_id')
        c_id = args.get('certificate_id')

        # 验证新增证书的项目是否存在
        pro = Project.query.filter(
            and_(Project.project_id == p_id, Project.project_id == User_projects.project_id,
                 User_projects.user_id == user_id)).all()
        if not pro:
            return jsonify(re_coder=RET.NODATA, msg="不存在该项目，请先添加项目！")

        # 验证新增证书的届次是否存在
        sessions = Session.query.filter(and_(Session.session_id == session_id, Session.project_id == p_id,
                                             User_sessions.session_id == Session.session_id,
                                             User_sessions.user_id == user_id)).all()
        if not sessions:
            return jsonify(re_code=RET.DBERR, msg="该届次不存在，请先添加新届次！")

        # 验证证书号是否唯一
        c_i = Certificate.query.filter(Certificate.certificate_id == c_id).first()
        if c_i:
            return jsonify(re_code=RET.DATAEXIST, msg="证书编号不能重复，请修改！")

        c_name = args.get('certificate_name')
        winner = args.get('winner')
        level = args.get('level')
        date = args.get('date')
        rank = args.get('rank')
        giver = args.get('giver')

        # 保存新增证书信息
        certificate = Certificate(certificate_id=c_id, certificate_name=c_name, winner=winner,
                                  level=level, date=date, rank=rank, giver=giver, user_id=user_id,
                                  project_id=p_id, session_id=session_id)
        db.session.add(certificate)
        db.session.commit()

        certificates = Certificate.query.filter(Certificate.user_id == user_id).all()
        return {'re_code': RET.OK, 'msg': '添加成功', 'certificates': marshal(certificates, Allcertificate_fields)}

    @is_login
    def put(self):  # 编辑证书
        user_id = g.user.user_id
        args = Allupdate_parser.parse_args()
        c_id = args.get('certificate_id')
        c_name = args.get('certificate_name')
        winner = args.get('winner')
        level = args.get('level')
        date = args.get('date')
        rank = args.get('rank')
        giver = args.get('giver')

        # 验证有无完全一致的证书
        certifi = Certificate.query.filter(and_(
            Certificate.certificate_name == c_name, Certificate.winner == winner, Certificate.level == level,
            Certificate.date == date, Certificate.rank == rank, Certificate.giver == giver)).first()
        if certifi:
            return jsonify(re_coder=RET.DATAEXIST, msg="该证书已存在，请修改！")

        # 获取需要修改的证书
        certificate = Certificate.query.get(c_id)

        # 修改并保存编辑后的证书
        certificate.certificate_name = c_name
        certificate.certificate_id = c_id
        certificate.winner = winner
        certificate.level = level
        certificate.date = date
        certificate.rank = rank
        certificate.giver = giver

        db.session.commit()

        certificates = Certificate.query.filter(Certificate.user_id == user_id).all()
        return {'re_code': RET.OK, 'msg': '修改成功', 'certificates': marshal(certificates, Allcertificate_fields)}

    @is_login
    def delete(self):  # 删除证书
        user_id = g.user.user_id
        args = Alldel_parser.parse_args()
        cid = args.get('certificate_id')

        # 获取需要删除的项目
        certificate = Certificate.query.filter(
            and_(Certificate.certificate_id == cid, Certificate.user_id == user_id)).first()

        db.session.delete(certificate)
        db.session.commit()

        certificates = Certificate.query.filter(Certificate.user_id == user_id).all()
        return {'re_code': RET.OK, 'msg': '删除成功', 'certificates': marshal(certificates, Allcertificate_fields)}

#导出单个证书
class ExportCertificate(Resource):
    @is_login
    def post(self):
        user_id = g.user.user_id

        args = ex_single_parser.parse_args()
        cid = args.get('certificate_id')
        pid=args.get('project_id')
        session_id=args.get('session_id')

        certificate = Certificate.query.filter(
            and_(Certificate.certificate_id == cid, Certificate.user_id == user_id,
                 Certificate.project_id == pid, Certificate.session_id == session_id)).first()
        return {'re_code': RET.OK, 'msg': '导出成功', 'certificate': marshal(certificate, certificate_fields)}


#上传excel批量导入证书
class ImportCertificates(Resource):
    @is_login
    def post(self):
        user_id = g.user.user_id
        args = im_parser.parse_args()
        file=args.get('file')
        f = file.read()
        clinic_file=xlrd.open_workbook(file_contents=f)
        table=clinic_file.sheet_by_index(0)
        rowNum=table.nrows #sheet行数

        for i in range(1,rowNum):
            newC = Certificate()
            row_data=table.row_values(i)
            newC.project_id = str(row_data[0])
            newC.session_id = str(row_data[1])
            newC.certificate_id = str(row_data[2])
            newC.level = str(row_data[3])
            newC.certificate_name = str(row_data[4])
            newC.winner = str(row_data[5])
            newC.rank = str(row_data[6])
            newC.giver = str(row_data[7])
            newC.date = str(row_data[8])
            newC.user_id = user_id

            # 验证新增证书的项目是否存在
            pro = Project.query.filter(
                and_(Project.project_id == newC.project_id, Project.project_id == User_projects.project_id,
                     User_projects.user_id == user_id)).all()
            if not pro:
                return jsonify(re_coder=RET.NODATA, msg="不存在该项目，请先添加项目！")

            # 验证新增证书的届次是否存在
            sessions = Session.query.filter(and_(Session.session_id == newC.session_id, Session.project_id == newC.project_id,
                                                 User_sessions.session_id == Session.session_id,
                                                 User_sessions.user_id == user_id)).all()
            if not sessions:
                return jsonify(re_code=RET.DBERR, msg="该届次不存在，请先添加新届次！")

            # 验证证书号是否唯一
            c_i = Certificate.query.filter(Certificate.certificate_id == newC.certificate_id).first()
            if c_i:
                return jsonify(re_code=RET.DATAEXIST, msg="证书编号不能重复，请修改！")
            db.session.add(newC)
            db.session.commit()

        certificates = Certificate.query.filter(
            Certificate.user_id == user_id,).first()
        return {'re_code': RET.OK, 'msg': '导入成功', 'certificates': marshal(certificates, Allcertificate_fields)}

#批量导出证书
# class ExportCertificates(Resource):
#      @is_login
#      def post(self):
#          user_id = g.user.user_id
#
#          args = ex_single_parser.parse_args()
#          cid = args.get('certificate_id')
#          pid = args.get('project_id')
#          session_id = args.get('session_id')
#
#          certificate = Certificate.query.filter(
#              and_(Certificate.certificate_id == cid, Certificate.user_id == user_id,
#                   Certificate.project_id == pid, Certificate.session_id == session_id)).first()
#          return {'re_code': RET.OK, 'msg': '导出成功', 'certificate': marshal(certificate, certificate_fields)}


api.add_resource(CertificateListApi, '/certificateList')
api.add_resource(AllCertificateListApi, '/allCertificateList')
api.add_resource(CertificateApi, '/certificate')
api.add_resource(AllCertificateApi,'/allCertificate')
api.add_resource(ExportCertificate, '/exportCertificate')
api.add_resource(ImportCertificates,'/importCertificates')
# api.add_resource(ExportCertificates, '/export_certificates')
