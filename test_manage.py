from test_app import app as app
from db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from tests.test_item_resource import test_item_resource
from tests.test_group_resource import test_group_resource
from tests.test_event_call_resource import test_event_call_resource
from tests.test_usage_resource import test_usage_resource
from tests.test_event_resource import test_event_resource
from tests.test_graph_resource import test_graph_resource
from tests import clear_database, seed_test_data

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run_tests():
    db.init_app(app)
    clear_database.clear_database()
    test_item_resource()
    test_group_resource()
    test_event_call_resource()
    test_usage_resource()
    test_event_resource()
    test_graph_resource()


if __name__ == '__main__':
    manager.run()
