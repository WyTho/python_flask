from app import app
from db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.Item import ItemModel
from models.Group import GroupModel
from models.ItemGroup import ItemGroupModel
from models.Usage import UsageModel
from models.UsageTypeEnum import UsageTypeEnum
from models.DataTypeEnum import DataTypeEnum
from models.Event import EventModel
from models.Graph import GraphModel
import random

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    print('Seeding...')
    db.init_app(app)
    if not ItemModel.find_by_id(1):
        items = []

        # START CREATING ITEMS
        items.append(ItemModel('Heating', '127.0.0.1:5000/item/1', 'comment'))
        items.append(UsageModel(1, UsageTypeEnum(UsageTypeEnum.KILOWATT), 5))

        items.append(ItemModel('staande_lamp_1', '127.0.0.1:5000/item/2', 'staande lamp = beste lamp'))
        items.append(UsageModel(2, UsageTypeEnum(UsageTypeEnum.KILOWATT), 1))

        items.append(ItemModel('staande_lamp_2', '127.0.0.1:5000/item/3', 'staande lamp = beste lamp'))
        items.append(UsageModel(3, UsageTypeEnum(UsageTypeEnum.KILOWATT), 1))

        items.append(ItemModel('slaapkamer_verlichting', '127.0.0.1:5000/item/4', 'verlichting in de slaapkamer'))
        items.append(UsageModel(4, UsageTypeEnum(UsageTypeEnum.KILOWATT), 1))

        items.append(ItemModel('lamp_nachtkastje', '127.0.0.1:5000/item/5', 'lamp op nachtkastje'))
        items.append(UsageModel(5, UsageTypeEnum(UsageTypeEnum.KILOWATT), 1))

        items.append(ItemModel('toilet', '127.0.0.1:5000/item/6', 'toilet in badkamer'))
        items.append(UsageModel(6, UsageTypeEnum(UsageTypeEnum.WATER_PER_USAGE), 9))

        items.append(ItemModel('douche', '127.0.0.1:5000/item/7', 'douche'))
        items.append(UsageModel(7, UsageTypeEnum(UsageTypeEnum.WATER_PER_HOUR), 9))

        items.append(ItemModel('vaatwasser', '127.0.0.1:5000/item/8', ''))
        items.append(UsageModel(8, UsageTypeEnum(UsageTypeEnum.WATER_PER_USAGE), 10))

        items.append(ItemModel('wasmachine', '127.0.0.1:5000/item/9', ''))
        items.append(UsageModel(9, UsageTypeEnum(UsageTypeEnum.WATER_PER_USAGE), 13))

        items.append(ItemModel('droger', '127.0.0.1:5000/item/10', ''))
        items.append(UsageModel(10, UsageTypeEnum(UsageTypeEnum.KILOWATT), 9))

        items.append(ItemModel('badkamer verlichting', '127.0.0.1:5000/item/11', ''))
        items.append(UsageModel(11, UsageTypeEnum(UsageTypeEnum.KILOWATT), 1))

        # START CREATING GROUPS
        items.append(GroupModel('Huiskamer', True))
        items.append(GroupModel('Slaapkamer', True))
        items.append(GroupModel('Badkamer', True))
        items.append(GroupModel('Verlichting', False))

        # START ADDING ITEMS TO GROUPS
        items.append(ItemGroupModel(2, 1))
        items.append(ItemGroupModel(3, 1))
        items.append(ItemGroupModel(8, 1))
        items.append(ItemGroupModel(4, 2))
        items.append(ItemGroupModel(5, 2))
        items.append(ItemGroupModel(6, 3))
        items.append(ItemGroupModel(7, 3))
        items.append(ItemGroupModel(9, 3))
        items.append(ItemGroupModel(10, 3))
        items.append(ItemGroupModel(11, 3))
        items.append(ItemGroupModel(2, 4))
        items.append(ItemGroupModel(3, 4))
        items.append(ItemGroupModel(4, 4))
        items.append(ItemGroupModel(5, 4))
        items.append(ItemGroupModel(11, 4))

        # START CREATING EVENTS
        timestamp = 1535760000
        while timestamp < 1539907200:
            for i in range(0, 24):
                for y in range(0, 10):
                    temp = 0
                    if i in [1, 2, 3, 4, 5, 15]:
                        temp = 15
                    elif i in [0, 14]:
                        temp = 16
                    elif i in [6, 12, 24, 13]:
                        temp = 18
                    elif i in [7, 8, 9, 17, 18, 19, 20, 21, 22]:
                        temp = 21
                    elif i in [10, 23]:
                        temp = 20
                    elif i in [11, 16]:
                        temp = 19

                    items.append(EventModel(1, DataTypeEnum(DataTypeEnum.TEMPERATURE), temp * random.uniform(0.9, 1.1), timestamp))
                    timestamp += 6 * 60

        items.append(GraphModel('AVERAGE_TEMPERATURE', DataTypeEnum(DataTypeEnum.TEMPERATURE)))

        for item in items:
            item.save_to_db()

if __name__ == '__main__':
    manager.run()