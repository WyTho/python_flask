from db import db


class EventModel(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    data_type = db.Column(db.String, nullable=False)
    data = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, item_id, data_type, data, timestamp):
        self.item_id = item_id
        self.data_type = data_type
        self.data = data
        self.timestamp = timestamp

    def to_json(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
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
    def find_all_by_item_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Event id:'{}', item_id:'{}', data_type:'{}', data:'{}', timestamp:'{}'>"\
            .format(self.id, self.item_id, self.data_type, self.data, self.timestamp)
