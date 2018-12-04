from models.Item import ItemModel
from models.Group import GroupModel
from models.ItemGroup import ItemGroupModel
from models.Usage import UsageModel
from models.UsageTypeEnum import UsageTypeEnum
from models.DataTypeEnum import DataTypeEnum
from models.Graph import GraphModel
from models.UnitEnum import UnitEnum


def seed_test_data():
    # @todo this doesn't work yet
    print('Seeding...')
    if not ItemModel.find_by_id(1):
        items = []

        # START CREATING ITEMS
        print('Creating items...')
        items.append(ItemModel('Heating', 'comment'))
        items.append(UsageModel(1, UsageTypeEnum.KILOWATT, 5, '127.0.0.1:5000/item/1', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('staande_lamp_1', 'staande lamp = beste lamp'))
        items.append(UsageModel(2, UsageTypeEnum.KILOWATT, 1, '127.0.0.1:5000/item/2', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('staande_lamp_2', 'staande lamp = beste lamp'))
        items.append(UsageModel(3, UsageTypeEnum.KILOWATT, 1, '127.0.0.1:5000/item/3', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('slaapkamer_verlichting', 'verlichting in de slaapkamer'))
        items.append(UsageModel(4, UsageTypeEnum.KILOWATT, 1, '127.0.0.1:5000/item/4', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('lamp_nachtkastje', 'lamp op nachtkastje'))
        items.append(UsageModel(5, UsageTypeEnum.KILOWATT, 1, '127.0.0.1:5000/item/5', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('toilet', 'toilet in badkamer'))
        items.append(UsageModel(6, UsageTypeEnum.WATER_PER_USAGE, 9,
                                '127.0.0.1:5000/item/6', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('douche', 'douche'))
        items.append(UsageModel(7, UsageTypeEnum.WATER_PER_HOUR, 9,
                                '127.0.0.1:5000/item/7', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('vaatwasser', ''))
        items.append(UsageModel(8, UsageTypeEnum.WATER_PER_USAGE, 10,
                                '127.0.0.1:5000/item/8', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('wasmachine', ''))
        items.append(UsageModel(9, UsageTypeEnum.WATER_PER_USAGE, 13,
                                '127.0.0.1:5000/item/9', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('droger', ''))
        items.append(UsageModel(10, UsageTypeEnum.KILOWATT, 9,
                                '127.0.0.1:5000/item/10', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        items.append(ItemModel('badkamer verlichting', ''))
        items.append(UsageModel(11, UsageTypeEnum.KILOWATT, 1,
                                '127.0.0.1:5000/item/11', UnitEnum(UnitEnum.TOGGLE), 0, 1))

        # START CREATING GROUPS
        print('Creating groups...')
        items.append(GroupModel('Huiskamer', True))
        items.append(GroupModel('Slaapkamer', True))
        items.append(GroupModel('Badkamer', True))
        items.append(GroupModel('Verlichting', False))

        # START ADDING ITEMS TO GROUPS
        print('Assigning items to groups...')
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

        items.append(GraphModel('AVERAGE_TEMPERATURE', DataTypeEnum(DataTypeEnum.TEMPERATURE)))
        items.append(GraphModel('AVERAGE_WATER_USAGE', DataTypeEnum(DataTypeEnum.WATER_USAGE)))

        print('inserting data into db, this may take a while...')
        current = 1
        total = len(items)
        for item in items:
            print('{} out of {}'.format(current, total))
            current += 1
            item.save_to_db()



