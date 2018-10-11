from db import db
from models import Hour


class DayModel(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer, primary_key=True)
    graph_id = db.Column(db.Integer, db.ForeignKey('graph.id'), nullable=False)
    date_timestamp = db.Column(db.Integer, nullable=False)
    hours = []

    def __init__(self, graph_id, date_timestamp):
        self.graph_id = graph_id
        self.date_timestamp = date_timestamp

    def to_json(self):
        return {
            'id': self.id,
            'values': [hour.value for hour in self.hours]
        }

    @classmethod
    def find_by_id(cls, day_id):
        day = cls.query.filter_by(id=day_id).first()
        day.events = Hour.HourModel.find_by_day_id(day.id)
        return day

    @classmethod
    def find_by_date_and_graph_id(cls, date_timestamp, graph_id):
        day = cls.query.filter_by(date_timestamp=date_timestamp, graph_id=graph_id).first()
        if day is None:
            day = DayModel(graph_id, date_timestamp)
            day.save_to_db()

        day.hours = Hour.HourModel.find_by_day_id(day.id)
        return day

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Day id:'{}'>".format(self.id)
