from db import db
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum


class UsageModel(db.Model):
    __tablename__ = '_usage'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('_item.id'))
    external_item_id = db.Column(db.Integer, nullable=False)
    consumption_type = db.Column(db.Enum(UsageTypeEnum), nullable=False)
    consumption_amount = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.Enum(UnitEnum), nullable=False)
    min_value = db.Column(db.Integer, nullable=True)
    max_value = db.Column(db.Integer, nullable=True)

    def __init__(self, item_id, external_item_id, consumption_type, consumption_amount, address, unit, min_value, max_value):
        self.item_id = item_id
        self.external_item_id = external_item_id
        self.consumption_type = consumption_type
        self.consumption_amount = consumption_amount
        self.address = address
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value

    def to_json(self):
        if self.id is None:
            url = "127.0.0.1:5000/api/usages/-1"
        else:
            url = "127.0.0.1:5000/api/usages/{}".format(self.id)
        return {
            'id': self.id,
            'item_id': self.item_id,
            'external_item_id': self.external_item_id,
            'consumption_type': self.consumption_type.value,
            'consumption_amount': self.consumption_amount,
            'address': self.address,
            'unit': self.unit.value,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'url': url
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, usage_id):
        return cls.query.filter_by(id=usage_id).first()

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

    def update(self, **kwargs):
        if kwargs['consumption_type']:
            self.consumption_type = kwargs['consumption_type']
        if kwargs['external_item_id']:
            self.external_item_id = kwargs['external_item_id']
        if kwargs['consumption_amount']:
            self.consumption_amount = kwargs['consumption_amount']
        if kwargs['address']:
            self.address = kwargs['address']
        if kwargs['unit']:
            self.unit = kwargs['unit']
        if kwargs['min_value']:
            self.min_value = kwargs['min_value']
        if kwargs['max_value']:
            self.max_value = kwargs['max_value']

        db.session.commit()
        return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.remove(self)
        db.session.commit()

    def __repr__(self):
        return "<Usage id:'{}'>"\
            .format(self.id)
