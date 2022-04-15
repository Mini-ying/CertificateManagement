# from sqlalchemy import and_
# from flask import Flask, request, session, flash, g, jsonify, render_template, make_response
# from flask_cors import CORS
# from response_code import RET
# from tools.check_login import is_login
# from models import *
# # from app_config import db
# # import app_config
# import xlrd
#
# # app=Flask(__name__,static_folder="../dist/static",template_folder="../dist")
# # app.config.from_object(app_config)
# # db.init_app(app)
# # CORS(app, supports_credentials=True)
#
#
# """
# 用户登录
# 退出登录
# 首页
# """
# # @app.route('/create_db')
# # def create_db():
# #     db.drop_all()
# #     db.create_all()
# #     return '创建成功'
#
# @app.route('/',methods=['POST'])
# def login():
#     """
#     登录
#     """
#     if request.method == 'POST':
#         userid = request.form.get('user_id')
#         password = request.form.get('password')
#
#         # 判断用户名和密码的是否填写
#         if not all([userid, password]):
#             return jsonify(re_code=RET.PARAMERR,msg="用户名或密码未填写")
#         # 检查用户名和密码是否一致
#         user = UserInfo.query.filter_by(user_id=userid, password=password).first()
#         # 如果一致
#         if user:
#             # 向session写入数据
#             session['user_id'] = user.user_id
#             session['username']=user.username
#             return jsonify(re_code=RET.OK,msg="登录成功")
#         else:
#             #用户名或密码不正确
#             return jsonify(re_code=RET.DATAERR,msg="用户名或密码错误")
#
#
#
# @app.route('/logout/', methods=['DELETE'])
# def logout():
#     """
#     退出登录
#     """
#     # 清空session
#     session.clear()
#     return jsonify(re_code=RET.OK,msg="已退出登录")
#
#
#
#
# # @app.route('/home/',methods=['GET'])
# # @is_login
# # def home():
# #     """
# #      首页
# #     """
# #     if request.method=='GET':
# #         return render_template('homepage.html')
#
# """
# 项目页面
# 查询项目
# 添加单个项目
# 编辑项目
# 删除项目
# """
# @app.route('/project',methods=["GET","POST"])
# @is_login
# def get_project_list():
#     #显示用户拥有的项目条目+搜索项目
#     if request.method=='POST':
#         user_id = session.get('user_id')
#         user = UserInfo.query.filter_by(user_id=user_id).first()
#
#         type=request.form.get('type')
#         info=request.form.get('info')
#         if type=='project_id': #通过项目编号查询
#             projects=Project.query.filter(and_(Project.project_id.contains(info),Project.project_id==User_projects.project_id,
#                                                User_projects.user_id==user_id)).all()
#             if projects:
#                 projects_list = []
#                 for project in projects:
#                     projects_list.append(project.to_dict())
#                 return jsonify(re_code=RET.OK, msg="查询成功", data={"projects": projects_list, "type": type})
#
#             else:
#                 return jsonify(re_code=RET.NODATA,msg="项目不存在")
#
#         if type=='project_name':  #通过项目名查询
#             projects=Project.query.filter(and_(Project.project_name.like('%'+info+'%'),Project.project_id==User_projects.project_id,
#                                                User_projects.user_id==user_id)
#                                           ).all()
#             if projects:
#                 projects_list = []
#                 for project in projects:
#                     projects_list.append(project.to_dict())
#                 return jsonify(re_code=RET.OK, msg="查询成功", data={"projects": projects_list, "type": type})
#
#             else:
#                 return jsonify(re_code=RET.NODATA, msg="项目不存在")
#
#     if request.method == 'GET':
#         user_id = session.get('user_id')
#         user=UserInfo.query.get(user_id)
#         projects = user.projects
#         projects_list = []
#         for project in projects:
#             projects_list.append(project.to_dict())
#         return jsonify(re_code=RET.OK, msg="查询成功", data={"projects": projects_list})
#
#
#
# @app.route("/addProject",methods=['POST'])
# @is_login
# def add_project():
#     #添加项目
#     p_id = request.form.get('project_id')
#     p_name = request.form.get('project_name')
#     user_id = session.get('user_id')
#
#     p_i = Project.query.filter(Project.project_id == p_id).first()
#     p_n = Project.query.filter(Project.project_name == p_name).first()
#
#     # 判断要添加的信息是否存在
#     if p_i:
#         return jsonify(re_coder=RET.DATAEXIST, msg="项目id不能重复，请修改！")
#     if p_n:
#         return jsonify(re_coder=RET.DATAEXIST, msg="项目名不能重复，请修改！")
#
#     # 保存新增项目信息
#     user = UserInfo.query.filter_by(user_id=user_id).first()
#     pj = Project(project_id=p_id, project_name=p_name)
#     pj.users.append(user)
#
#     db.session.add(pj)
#     db.session.commit()
#
#     projects = user.projects
#     projects_list = []
#     for project in projects:
#         projects_list.append(project.to_dict())
#     return jsonify(re_code=RET.OK, msg="添加成功", data={"projects": projects_list})
#
#
# @app.route('/edit_project/',methods=['POST'])
# @is_login
# def edit_project():
#     #编辑项目信息
#     if request.method=='POST':
#         #获取需要修改的项目id
#         p_id=request.form.get('project_id')
#         project_list=UserInfo.query.filter_by(id=g.id).first().user_project.all()
#         project = project_list.query.filter(Project.project_id == p_id).first()
#
#         #修改并保存编辑后的项目
#         p_name = request.form.get('project_name')
#         project.project_name=p_name
#         db.session.commit()
#
#         user_id = session.get('user_id')
#         # p_id=request.form.get('project_id')
#         # p_name=request.form.get('project_name')
#
#         p_i=Project.query.filter(Project.project_id==p_id).first()
#         p_n=Project.query.filter(Project.project_name==p_name).first()
#
#         #判断要添加的信息是否存在
#         if p_i:
#             return jsonify(re_coder=RET.DATAEXIST,msg="项目id不能重复，请修改！")
#         if p_n:
#             return jsonify(re_coder=RET.DATAEXIST,msg="项目名不能重复，请修改！")
#
#         #保存新增项目信息
#         user=UserInfo.query.filter_by(user_id=user_id).first()
#         project=Project(project_id=p_id,project_name=p_name)
#
#         user.relate_course.append(project)
#         db.session.commit()
#
#         user_id = session.get('user_id')
#         user = UserInfo.query.filter_by(user_id=user_id)
#         projects = user.projects
#         projects_list = []
#         for project in projects:
#             projects_list.append(project.to_dict())
#         return jsonify(re_code=RET.OK, msg="添加成功", data={"projects": projects_list})
#
#
# #删除项目
# @app.route("/deleteProject/",methods=["POST"])
# @is_login
# def deleteProject():
#     pid=request.form.get('project_id')
#     user_id=session.get('user_id')
#     project=Project.query.get(pid)
#     user=UserInfo.query.get(user_id)
#
#     user.projects.remove(project)
#     db.session.delete(project)
#     db.session.commit()
#
#     projects = user.projects
#     projects_list = []
#     for project in projects:
#         projects_list.append(project.to_dict())
#     return jsonify(re_code=RET.OK, msg="删除成功", data={"projects": projects_list})
#
#
#
# # """
# # 届次页面（搜索+显示）
# # 添加届次
# # """
# # @app.route('/sessions/',methods=['GET','POST'])
# # @is_login
# # def get_sessions_list():
# #     #搜索项目的不同届次
# #     if request.method=='POST':
# #         type = request.form.get('type')
# #         info = request.form.get('info')
# #         if type == 'sessions':  # 通过届次查询
# #             certificates = Certificate.query.filter(Certificate.sessions.contains(info)
# #                                                     ).with_entities(Certificate.sessions,Certificate.certificate_name
# #                                                            ).all()
# #             if certificates is None:
# #                 return jsonify(re_code=RET.NODATA,msg="不存在该届次")
# #
# #             certificates_list = []
# #             for certificate in certificates:
# #                 certificates_list.append(certificate.certificate_to_dict())
# #             return jsonify(re_code=RET.OK, msg="查询成功", data={"certificates": certificates_list})
# #
# #         if type == 'certificate_name':  # 通过证书名查询
# #             certificates = Certificate.query.with_entities(Certificate.sessions,Certificate.certificate_name
# #                                                            ).filter_by(Certificate.certificate_name.like('%'+info+'%')).all()
# #             if certificates is None:
# #                 return jsonify(re_code=RET.NODATA,msg="证书不存在")
# #             certificates_list = []
# #             for certificate in certificates:
# #                 certificates_list.append(certificate.certificate_to_dict())
# #             return jsonify(re_code=RET.OK, msg="查询成功", data={"certificates": certificates_list})
# #
# #     # 显示项目的不同届次
# #     if request.method == 'GET':
# #         user_id = session.get('user_id')
# #         certificates = Certificate.query.with_entities(Certificate.sessions,Certificate.certificate_name
# #                                                            ).filter(Certificate.user_id == user_id
# #                                                                    ).order_by(
# #             and_(Certificate.certificate_id, Certificate.sessions)).all()
# #
# #         certificates_list = []
# #         for certificate in certificates:
# #             certificates_list.append(certificate.sessions_to_dict())
# #         return jsonify(re_code=RET.OK, msg="查询成功", data={"certificates": certificates_list})
# #
# #
# #
# # @app.route("/addSessions/",methods=['POST'])
# # @is_login
# # def add_sessions():
# #     #添加届次
# #     if request.method=='POST':
# #         s=request.form.get('sessions')
# #         c_id=Certificate.query.with_entities(Certificate.certificate_id
# #                                              ).filter(Certificate.sessions==s).first()
# #         certificate=Certificate.query.filter(Project.certificate_id==c_id).first()
# #
# #         #判断要添加的信息是否存在
# #         if certificate:
# #             return jsonify(re_code=RET.DATAEXIST,msg="届次不能重复，请修改！")
# #
# #         sessions=request.form.get('sessions')
# #         c_name = request.form.get('certificate_name')
# #
# #
# #         #保存新增证书信息
# #         certificate=Certificate(certificate_id=c_id,certificate_name=c_name,sessions=sessions,user_id = g.id)
# #         db.session.add(certificate)
# #         db.session.commit()
# #         flash("添加届次成功")
# #
# #         user_id = session.get('user_id')
# #         certificates = Certificate.query.with_entities(Certificate.sessions, Certificate.certificate_name
# #                                                        ).filter_by(Certificate.user_id == user_id
# #                                                                    ).order_by(
# #             and_(Certificate.certificate_id, Certificate.sessions)).all()
# #
# #         certificates_list = []
# #         for certificate in certificates:
# #             certificates_list.append(certificate.certificate_to_dict())
# #         return jsonify(re_code=RET.OK, msg="添加成功", data={"certificates": certificates_list})
#
# """
# 证书页面
# 查询证书
# 添加证书
# 编辑证书
# 删除证书
# 批量导入该届次证书
# 导出单个证书
# 导出多个勾选证书
# """
# @app.route('/certificate/',methods=['GET','POST'])
# @is_login
# def get_certificate_list():
#     #搜索证书
#     if request.method == 'POST':
#         user_id = session.get('user_id')
#         type = request.form.get('type')
#         info = request.form.get('info')
#         if type == 'certificate_id': #通过证书编号查询
#             certificates = Certificate.query.filter(and_(
#                 Certificate.certificate_id.contains(info),Certificate.user_id==user_id)).all()
#
#             if certificates:
#                 certificates_list = []
#                 for certificate in certificates:
#                     certificates_list.append(certificate.certificate_to_dict())
#                 return jsonify(re_code=RET.OK, msg="搜索成功", data={"certificates": certificates_list})
#
#             else:
#                 return jsonify(re_code=RET.NODATA, msg="证书不存在")
#
#         if type == 'certificate_name': #通过证书名查询
#             certificates = Certificate.query.filter(and_(
#                 Certificate.certificate_name.contains(info),Certificate.user_id==user_id
#             )).all()
#
#             if certificates:
#                 certificates_list = []
#                 for certificate in certificates:
#                     certificates_list.append(certificate.certificate_to_dict())
#                 return jsonify(re_code=RET.OK, msg="搜索成功", data={"certificates": certificates_list})
#
#             else:
#                 return jsonify(re_code=RET.NODATA, msg="证书不存在")
#
#         if type == 'winner': #通过获奖者查询
#             certificates = Certificate.query.filter(and_(
#                 Certificate.winner.like('%' + info + '%'),Certificate.user_id==user_id)).all()
#             if certificates:
#                 certificates_list = []
#                 for certificate in certificates:
#                     certificates_list.append(certificate.certificate_to_dict())
#                 return jsonify(re_code=RET.OK, msg="搜索成功", data={"certificates": certificates_list})
#
#             else:
#                 return jsonify(re_code=RET.NODATA, msg="证书不存在")
#
#     # 显示用户证书条目
#     if request.method == 'GET':
#         user_id = session.get('user_id')
#         # sessions = session.get('sessions')
#         # certificates = Certificate.query.filter(and_(Certificate.user_id == user_id, Certificate.sessions == sessions
#         #                                                 )).order_by(Certificate.certificate_id).all()
#         certificates = Certificate.query.filter(Certificate.user_id == user_id
#                                                      ).order_by(and_(Certificate.sessions,Certificate.certificate_id)).all()
#         certificates_list = []
#         for certificate in certificates:
#             certificates_list.append(certificate.certificate_to_dict())
#         return jsonify(re_code=RET.OK, msg="查询成功", data={"certificates": certificates_list})
#
#
# @app.route("/addCertificate/",methods=['POST'])
# @is_login
# def addCertificate():
#     #添加证书
#     if request.method=='POST':
#         user_id = session.get('user_id')
#
#         c_id=request.form.get('certificate_id')
#         c_i=Certificate.query.filter(Certificate.certificate_id==c_id).first()
#         #判断要添加的信息是否存在
#         if c_i:
#             return jsonify(re_code=RET.DATAEXIST,msg="证书编号不能重复，请修改！")
#
#         project_id = request.form.get('project_id')
#         project=Project.query.filter_by(project_id=project_id)
#         if project is None:
#             return jsonify(re_code=RET.DBERR,msg="该项目不存在，请先添加新项目！")
#
#         sessions=request.form.get('sessions')
#         c_name = request.form.get('certificate_name')
#         winner=request.form.get('winner')
#         level = request.form.get('level')
#         date = request.form.get('date')
#         rank = request.form.get('rank')
#         giver=request.form.get('giver')
#
#         #保存新增证书信息
#         certificate=Certificate(certificate_id=c_id,certificate_name=c_name,sessions=sessions,winner=winner,level=level,date=date,rank=rank,giver=giver,user_id =user_id,project_id=project_id)
#         db.session.add(certificate)
#         db.session.commit()
#         flash("添加成功")
#
#         # sessions = session.get('sessions')
#         certificates = Certificate.query.filter(and_(Certificate.user_id == user_id, Certificate.sessions == sessions
#                                                         )).order_by(Certificate.certificate_id).all()
#         certificates_list = []
#         for certificate in certificates:
#             certificates_list.append(certificate.certificate_to_dict())
#         return jsonify(re_code=RET.OK, msg="添加成功", data={"certificates": certificates_list})
#
#
#
# #删除证书
# @app.route("/deleteCertificate/",methods=["DELETE"])
# @is_login
# def deleteCertificate():
#     user_id = session.get('user_id')
#     cid=request.form.get('certificate_id')
#     certificate=Certificate.query.filter(and_(Certificate.certificate_id==cid,Certificate.user_id==user_id)).first()
#
#     db.session.delete(certificate)
#     db.session.commit()
#
#     certificates = Certificate.query.filter(Certificate.user_id == user_id
#                                             ).order_by(and_(Certificate.sessions, Certificate.certificate_id)).all()
#     certificates_list = []
#     for certificate in certificates:
#         certificates_list.append(certificate.certificate_to_dict())
#     return jsonify(re_code=RET.OK, msg="删除成功", data={"certificates": certificates_list})
#
#
#
# @app.route('/edit_certificate/',methods=['POST'])
# @is_login
# def edit_certificate():
#     #编辑证书信息
#     user_id = session.get('user_id')
#     if request.method=='POST':
#         #获取需要修改的证书id
#         c_id=request.form.get('certificate_id')
#         certificate=Certificate.query.filter(
#             and_(Certificate.certificate_id==c_id,Certificate.user_id==user_id)).first()
#
#         #修改并保存编辑后的项目
#         c_name = request.form.get('certificate_name')
#         sessions=request.form.get('sessions')
#         winner = request.form.get('winner')
#         level = request.form.get('level')
#         date = request.form.get('date')
#         rank = request.form.get('rank')
#         giver = request.form.get('giver')
#
#         certificate.certificate_name=c_name
#         certificate.certificate_id=c_id
#         certificate.sessions=sessions
#         certificate.winner=winner
#         certificate.level=level
#         certificate.date=date
#         certificate.rank=rank
#         certificate.giver=giver
#
#         db.session.commit()
#         flash('修改成功')
#
#         sessions = session.get('sessions')
#         certificates = Certificate.query.filter_by(and_(Certificate.user_id == user_id, Certificate.sessions == sessions
#                                                         )).order_by(Certificate.certificate_id).all()
#         certificates_list = []
#         for certificate in certificates:
#             certificates_list.append(certificate.certificate_to_dict())
#         return jsonify(re_code=RET.OK, msg="编辑成功", data={"certificates": certificates_list})
#
#
#
# @app.route('/import_certificate/',methods=['GET','POST'])
# @is_login
# def importCertificate():
#     #批量导入该届次名单
#     if request.method=='POST':
#         user_id = session.get('user_id')
#         project_id=request.form.get('project_id')
#         file=request.files.get('file')
#         f=file.read()
#         clinic_file=xlrd.open_workbook(file_contents=f)
#         table=clinic_file.sheet_by_index(0)
#         rowNum=table.nrows #sheet行数
#         colNum=table.ncols #sheet列数
#
#         list=[]
#         for i in range(rowNum):
#             rowlist=[]
#             for j in range(colNum):
#                 rowlist.append(table.cell_value(i,j))
#             list.append(rowlist)
#             del list[0]  #删掉第一行，第一行是文件头
#
#             #将数据插入到数据库
#             with db.auto_commit():
#                 for a in list:
#                     newC = Certificate()
#                     newC.certificate_id=a[0]
#                     newC.sessions=a[1]
#                     newC.level=a[2]
#                     newC.certificate_name=a[3]
#                     newC.winner=a[4]
#                     newC.rank=a[5]
#                     newC.giver=a[6]
#                     newC.date=a[7]
#                     newC.project_id = project_id
#                     newC.user_id=user_id
#                     db.session.add(newC)
#                     db.session.commit()
#                 flash('导入成功')
#
#     certificates = Certificate.query.filter_by(Certificate.user_id == user_id
#                                                ).order_by(Certificate.certificate_id).all()
#     certificates_list = []
#     for certificate in certificates:
#         certificates_list.append(certificate.certificate_to_dict())
#     return jsonify(re_code=RET.OK, msg="导入成功", data={"certificates": certificates_list})
#
# @app.route('/export_single_certificate/',methods=['POST'])
# @is_login
# def ExportSingleCertificate():
#     #导出单个证书
#     if request.method=='POST':
#         user_id = session.get('user_id')
#         c_id=request.form.get('certificate_id')
#         certificate = Certificate.query.filter(
#             and_(Certificate.user_id == user_id,Certificate.certificate_id==c_id)).first()
#         return jsonify(re_code=RET.OK,msg="导出成功",data={"certificate":certificate.certificate_to_dict()})
#
# # @app.route('/export_certificates/',methods=['POST'])
# # @is_login
# # def ExportCertificates():
# #     #导出多个勾选证书
# #     user_id = session.get('user_id')
# #     sessions = session.get('sessions')
# #     certificates=[]
# #
# #     if request.method=='POST':
# #         c_ids=request.values.getlist("s_option")
# #         for c_id in c_ids:
# #             certificate = Certificate.query.filter_by(
# #                 and_(Certificate.user_id == user_id, Certificate.sessions == sessions,Certificate.certificate_id==c_id)).first()
# #             certificates.append(certificate)
# #         certificates_list = []
# #         for certificate in certificates:
# #             certificates_list.append(certificate.certificate_to_dict())
# #         return jsonify(re_code=RET.OK, msg="导出成功", data={"certificates": certificates_list})
#
#
#
#
