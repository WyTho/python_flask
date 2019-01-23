from db import db
from models.Usage import UsageModel
from models.Event import EventModel
from . import ItemGroup


class ItemModel(db.Model):
    __tablename__ = '_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    last_use = None
    usages = []
    groups = []

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment
        self.usages = UsageModel.find_all_by_item_id(self.id)
        self.fill_status()
        self.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(self.id)

    def to_json(self):
        if self.id is None:
            url = "127.0.0.1:5000/api/v1/items/-1"
        else:
            url = "127.0.0.1:5000/api/v1/items/{}".format(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'comment': self.comment,
            'last_use': self.last_use,
            'usages': [usage.to_json() for usage in self.usages],
            'groups': [{'id': group.id, 'name': group.name} for group in self.groups],
            'url': url
        }

    @classmethod
    def find_all(cls):
        items = cls.query.all()
        for item in items:
            item.usages = UsageModel.find_all_by_item_id(item.id)
            item.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(item.id)
            item.fill_status()
        return items

    @classmethod
    def find_by_id(cls, item_id):
        item = cls.query.filter_by(id=item_id).first()
        if not item:
            return item
        item.usages = UsageModel.find_all_by_item_id(item.id)
        item.groups = ItemGroup.ItemGroupModel.find_groups_by_item_id(item.id)
        item.fill_status()
        return item

    @classmethod
    def find_by_id_without_groups(cls, item_id):
        item = cls.query.filter_by(id=item_id).first()
        item.usages = UsageModel.find_all_by_item_id(item_id)
        item.fill_status()
        return item

    def fill_status(self):
        last_event = None
        for usage in self.usages:
            event = EventModel.find_latest_by_usage_id(usage.id)
            if event is None:
                pass
            elif last_event is None:
                last_event = event
            elif last_event.timestamp > event:
                last_event = event

        if last_event is not None:
            usage = UsageModel.find_by_id(last_event.usage_id)
            self.last_use = {
                'last_use_timestamp': last_event.timestamp,
                'data_type': usage.unit.value,
                'data': float(last_event.data),
                'usage_id': last_event.usage_id
            }

    def has_usage(self, usage_id):
        for usage in self.usages:
            if usage.id == usage_id:
                return True
        return False

    def is_in_module(self):
        for group in self.groups:
            if group.is_module:
                return True
        return False

    def is_in_this_group(self, group_id):
        for group in self.groups:
            if group.id == group_id:
                return True
        return False

    def update(self, **kwargs):
        if kwargs['name']:
            self.name = kwargs['name']
        if kwargs['comment']:
            self.comment = kwargs['comment']

        db.session.commit()
        return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Item id:'{}'>".format(self.id)
