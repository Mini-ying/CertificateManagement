from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from backend.models import *
from backend import create_app, db

app = create_app()
manager=Manager(app=app)

#命令工具
migrate=Migrate(app=app,db=db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
