from db import db
from . import ItemGroup


class GroupModel(db.Model):
    __tablename__ = '_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_module = db.Column(db.Boolean, default=False)
    items = []

    def __init__(self, name, is_module):
        self.name = name
        self.is_module = is_module
        self.items = ItemGroup.ItemGroupModel.find_items_by_group_id(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_module': self.is_module,
            'items': [
                {
                    'id': item.id,
                    'name': item.name,
                    'comment': item.comment,
                } for item in self.items],
        }

    @classmethod
    def find_all(cls):
        groups = cls.query.all()
        for group in groups:
            group.items = ItemGroup.ItemGroupModel.find_items_by_group_id(group.id)
        return groups

    @classmethod
    def find_by_id(cls, group_id):
        group = cls.query.filter_by(id=group_id).first()
        if group is None:
            return None
        group.items = ItemGroup.ItemGroupModel.find_items_by_group_id(group.id)
        return group

    @classmethod
    def find_by_id_without_items(cls, group_id):
        return cls.query.filter_by(id=group_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        item_groups = ItemGroup.ItemGroupModel.find_by_group_id(self.id)
        for item_group in item_groups:
            item_group.delete_from_db()

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Group name:'{}'>".format(self.name)
