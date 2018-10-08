from db import db
import time


class EventCallModel(db.Model):
    __tablename__ = 'event_call'
    id = db.Column(db.Integer, primary_key=True)
    json = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __init__(self, json):
        self.json = json
        self.timestamp = time.time()

    def to_json(self):
        return {
            'id': self.id,
            'json': self.json,
            'timestamp': self.timestamp
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, event_call_id):
        return cls.query.filter_by(id=event_call_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<EventCall id:'{}'>".format(self.id)
