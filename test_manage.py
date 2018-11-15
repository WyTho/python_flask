from test_app import app as app
from db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from tests.test_item_resource import test_item_resource

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run_tests():
    db.init_app(app)
    test_item_resource()


if __name__ == '__main__':
    manager.run()
