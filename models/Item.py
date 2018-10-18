from db import db
from models.Usage import UsageModel
from . import ItemGroup


class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    usages = []
    groups = []

    def __init__(self, name, address, comment):
        self.name = name
        self.address = address
        self.comment = comment
        self.events = UsageModel.find_all_by_item_id(self.id)
        self.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'comment': self.comment,
            'usages': [usage.to_json() for usage in self.usages],
            'groups': [{'id': group.id, 'name': group.name} for group in self.groups]
        }

    @classmethod
    def find_all(cls):
        items = cls.query.all()
        for item in items:
            item.usages = UsageModel.find_all_by_item_id(item.id)
            item.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(item.id)
        return items

    @classmethod
    def find_by_id(cls, item_id):
        item = cls.query.filter_by(id=item_id).first()
        if not item:
            return item
        item.usages = UsageModel.find_all_by_item_id(item.id)
        item.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(item.id)
        return item

    @classmethod
    def find_by_id_without_groups(cls, item_id):
        item = cls.query.filter_by(id=item_id).first()
        item.usages = UsageModel.find_all_by_item_id(item_id)
        return item

    def is_in_module(self):
        for group in self.groups:
            if group.is_module:
                return True
        return False

    def update(self, **kwargs):
        if kwargs['name']:
            self.name = kwargs['name']
        if kwargs['address']:
            self.address = kwargs['address']
        if kwargs['comment']:
            self.comment = kwargs['comment']

        db.session.commit()
        return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Item name:'{}', address:'{}', comment:'{}'>".format(self.name, self.address, self.comment)
