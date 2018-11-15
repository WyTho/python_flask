from db import db
from models.DataTypeEnum import DataTypeEnum


class EventModel(db.Model):
    __tablename__ = '_event'
    id = db.Column(db.Integer, primary_key=True)
    usage_id = db.Column(db.Integer, db.ForeignKey('_usage.id'))
    data_type = db.Column(db.Enum(DataTypeEnum), nullable=False)
    data = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, usage_id, data_type, data, timestamp):
        self.usage_id = usage_id
        self.data_type = data_type
        self.data = data
        self.timestamp = timestamp

    def to_json(self):
        return {
            'id': self.id,
            'usage_id': self.usage_id,
            'data_type': self.data_type,
            'data': self.data,
            'timestamp': self.timestamp
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, event_id):
        return cls.query.filter_by(id=event_id).first()

    @classmethod
    def find_all_by_usage_id(cls, usage_id):
        return cls.query.filter_by(usage_id=usage_id).all()

    @classmethod
    def filter(cls, **kwargs):

        results = cls.query
        if 'usage_id' in kwargs:
            results = results.filter_by(usage_id=kwargs['usage_id'])
        if 'data_type' in kwargs:
            results = results.filter_by(data_type=kwargs['data_type'])
        if 'after_timestamp' in kwargs:
            results = results.filter(EventModel.timestamp > kwargs['after_timestamp'])
        if 'before_timestamp' in kwargs:
            results = results.filter(EventModel.timestamp < kwargs['before_timestamp'])

        return results.all()

    @classmethod
    def find_latest_by_usage_id(cls, usage_id):
        return cls.query.filter_by(usage_id=usage_id).order_by(EventModel.timestamp.desc()).first()

    @classmethod
    def find_next_false(cls, event):
        return cls.query\
            .filter(EventModel.timestamp > event.timestamp)\
            .filter(EventModel.usage_id == event.usage_id)\
            .filter_by(data='False').first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Event id:'{}', usage_id:'{}', data_type:'{}', data:'{}', timestamp:'{}'>"\
            .format(self.id, self.usage_id, self.data_type, self.data, self.timestamp)
