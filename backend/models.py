from backend.app_config import db
import datetime


# user_projects为用户和项目多对多的关联表
class User_projects(db.Model):
    __tablename__ = "user_projects"
    __table_args__ = {"extend_existing": True}
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.VARCHAR(36), db.ForeignKey('userinfo.user_id'))
    project_id = db.Column(db.VARCHAR(36), db.ForeignKey('project.project_id'))


# user_sessions为用户和届次多对多的关联表
class User_sessions(db.Model):
    __tablename__ = "user_sessions"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.VARCHAR(36), db.ForeignKey('userinfo.user_id'))
    session_id = db.Column(db.VARCHAR(36), db.ForeignKey('session.session_id'))


#用户类
class UserInfo(db.Model):
    __tablename__ = "userinfo"
    __table_args__ = {"extend_existing": True}
    user_id = db.Column(db.VARCHAR(36), primary_key=True,unique=True,nullable=False)
    username = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(512), nullable=False)
    phone=db.Column(db.VARCHAR(512),unique=True)
    role=db.Column(db.VARCHAR(512),nullable=False)#用户权限，为普通用户ordinary user还是管理员administrator
    # email = db.Column(db.VARCHAR(512), nullable=False)
    # permanent_token = db.Column(db.VARCHAR(1024))
    # available = db.Column(db.BOOLEAN)
    # addition_info = db.Column(db.JSON)
    # created_at = db.Column(db.DATETIME, default=datetime.now)
    # updated_at = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    #用户和证书一对多的关系
    certificates=db.relationship("Certificate",backref="userinfo")

    # def __init__(self, user_id,username,password):
    #     self.user_id = user_id
    #     self.username = username
    #     self.password = password
    #
    # def to_dict(self):
    #     """转换为字典数据"""
    #     user_dict = {
    #         "user_id": self.user_id,
    #         "username": self.username,
    #         "password": self.password
    #     }
    #     return user_dict

#证书类
class Certificate(db.Model):
    __tablename__ = "certificate"
    __table_args__ = {"extend_existing": True}
    # sessions=db.Column(db.VARCHAR(512),nullable=False)#届次
    certificate_id=db.Column(db.VARCHAR(36),primary_key=True,unique=True) #证书编号
    certificate_name=db.Column(db.VARCHAR(512)) #证书名称
    level = db.Column(db.VARCHAR(64))  # 证书级别
    winner=db.Column(db.VARCHAR(64)) #获奖者名称
    rank = db.Column(db.VARCHAR(512))  # 获奖名次
    date=db.Column(db.DateTime) #获奖日期
    giver=db.Column(db.VARCHAR(512)) #颁奖机构

    # 用户和证书的一对多的关联关系（相当于外键）
    user_id = db.Column(db.VARCHAR(36), db.ForeignKey('userinfo.user_id'))

    #项目和证书一对多的关系（相当于外键）
    project_id = db.Column(db.VARCHAR(36), db.ForeignKey('project.project_id'))

    #届次和证书的一对多关系（相当于外键）
    session_id = db.Column(db.VARCHAR(36), db.ForeignKey('session.session_id'))

    # def __init__(self, sessions,certificate_id,winner,level,date,rank,certificate_name,giver,user_id,project_id):
    #     self.sessions = sessions
    #     self.certificate_id = certificate_id
    #     self.winner = winner
    #     self.level = level
    #     self.date = date
    #     self.rank = rank
    #     self.certificate_name = certificate_name
    #     self.giver = giver
    #     self.user_id = user_id
    #     self.project_id=project_id
    #
    # def certificate_to_dict(self):
    #     """转换为字典数据"""
    #     certificate_dict = {
    #         "sessions": self.sessions,
    #         "certificate_id": self.certificate_id,
    #         "winner": self.winner,
    #         "level": self.level,
    #         "date": self.date.strftime("%Y-%m-%d"),
    #         "rank": self.rank,
    #         "certificate_name": self.certificate_name,
    #         "giver": self.giver
    #     }
    #     return certificate_dict
    #
    # def sessions_to_dict(self):
    #     sessions_dict={
    #         "sessions": self.sessions,
    #         "certificate_name": self.certificate_name
    #     }
    #     return sessions_dict

#届次类
class Session(db.Model):
    __tablename__="session"
    __table_args__ = {"extend_existing": True}
    session_id = db.Column(db.VARCHAR(36), primary_key=True) #届次id
    number=db.Column(db.VARCHAR(36),nullable=False) #第x届
    category=db.Column(db.VARCHAR(36)) #届次类别

    # 项目和届次一对多的关系（相当于外键）
    project_id = db.Column(db.VARCHAR(36), db.ForeignKey('project.project_id'))

    #届次和证书的一对多关系
    certificates = db.relationship('Certificate', backref='session', foreign_keys=[Certificate.session_id])

    #用户和届次的多对多关系
    users = db.relationship('UserInfo', backref='sessions', secondary='user_sessions')


    # def __init__(self, number,category):
    #     self.number = number
    #     self.category = category


#项目类
class Project(db.Model):
    __tablename__="project"
    __table_args__ = {"extend_existing": True}
    project_id=db.Column(db.VARCHAR(36), primary_key=True) #项目id
    project_name = db.Column(db.VARCHAR(512))  # 项目名称

    #用户和项目多对多的关系
    users=db.relationship('UserInfo',backref='projects',secondary='user_projects')

    # 项目和证书一对多的关系
    certificates = db.relationship('Certificate', backref='project',foreign_keys=[Certificate.project_id])

    #项目和届次的一对多关系
    sessions=db.relationship('Session', backref='project',foreign_keys=[Session.project_id])

    # def __init__(self, project_id,project_name):
    #     self.project_id = project_id
    #     self.project_name = project_name
    #
    #
    # def to_dict(self):
    #     """转换为字典数据"""
    #     project_dict = {
    #         "project_id": self.project_id,
    #         "project_name": self.project_name
    #     }
    #     return project_dict






