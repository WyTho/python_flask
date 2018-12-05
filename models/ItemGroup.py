from db import db
from . import Group
from . import Item


class ItemGroupModel(db.Model):
    __tablename__ = '_item_group'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('_item.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('_group.id'))

    def __init__(self, item_id, group_id):
        self.item_id = item_id
        self.group_id = group_id

    def to_json(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'group_id': self.group_id
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_group_id(cls, group_id):
        return cls.query.filter_by(id=group_id).all()

    @classmethod
    def find_groups_by_item_id(cls, item_id):
        item_groups = cls.query.filter_by(item_id=item_id).all()
        groups = []
        for item_group in item_groups:
            groups.append(Group.GroupModel.find_by_id_without_items(item_group.group_id))
        return groups

    @classmethod
    def find_items_by_group_id(cls, group_id):
        item_groups = cls.query.filter_by(group_id=group_id).all()
        items = []
        for item_group in item_groups:
            items.append(Item.ItemModel.find_by_id_without_groups(item_id=item_group.item_id))
        return items

    @classmethod
    def find_by_group_id_and_item_id(cls, item_id, group_id):
        item_group = cls.query.filter_by(group_id=group_id).filter_by(item_id=item_id).first()
        return item_group

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Group name:'{}'>".format(self.name)
