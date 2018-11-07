from db import db
from models.UsageTypeEnum import UsageTypeEnum
from models.Event import EventModel


class UsageModel(db.Model):
    __tablename__ = 'usage'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    usage_type = db.Column(db.Enum(UsageTypeEnum), nullable=False)
    usage = db.Column(db.String, nullable=False)

    def __init__(self, item_id, usage_type, usage):
        self.item_id = item_id
        self.usage_type = usage_type
        self.usage = usage

    def to_json(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'usage_type': self.usage_type.value,
            'usage': self.usage
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, event_id):
        return cls.query.filter_by(id=event_id).first()

    @classmethod
    def find_all_by_item_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()

    @classmethod
    def filter(cls, **kwargs):
        results = cls.query
        if 'item_id' in kwargs:
            results = results.filter_by(item_id=kwargs['item_id'])
        if 'usage_type' in kwargs:
            results = results.filter_by(usage_type=kwargs['data_type'].value)

        return results.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Usage id:'{}', item_id:'{}', usage_type:'{}', usage:'{}'>"\
            .format(self.id, self.item_id, self.usage_type.value, self.usage)
