from db import db
from models import Hour


class DayModel(db.Model):
    __tablename__ = '_day'
    id = db.Column(db.Integer, primary_key=True)
    graph_id = db.Column(db.Integer, db.ForeignKey('_graph.id'), nullable=False)
    date_timestamp = db.Column(db.Integer, nullable=False)
    hours = []

    def __init__(self, graph_id, date_timestamp):
        self.graph_id = graph_id
        self.date_timestamp = date_timestamp

    def to_json(self):
        if len(self.hours) == 0:
            return {
                'id': self.id,
                'timestamp': self.date_timestamp,
                'values': [None for i in range(24)]
            }
        return {
            'id': self.id,
            'timestamp': self.date_timestamp,
            'values': [hour.value for hour in self.hours]
        }

    @classmethod
    def find_by_id(cls, day_id):
        day = cls.query.filter_by(id=day_id).first()
        day.hours = Hour.HourModel.find_by_day_id(day.id)
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

    def set_hours(self, hours):
        self.hours = hours

    def add_hour(self, hour):
        self.hours.append(hour)
        self.organize_hours()

    def organize_hours(self):
        sorted_hours = []
        for i in range(0, 24):
            for hour in self.hours:
                if hour.hour == i:
                    sorted_hours.append(hour)
        self.hours = sorted_hours

    def has_24_hours(self):
        return len(self.hours) == 24

    def __repr__(self):
        return "<Day id:'{}'>".format(self.id)
