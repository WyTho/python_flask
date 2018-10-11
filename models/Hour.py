from db import db


class HourModel(db.Model):
    __tablename__ = 'hour'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, day_id, hour, value):
        self.day_id = day_id
        self.hour = hour
        self.value = value

    def to_json(self):
        return {
            'id': self.id,
            'day_id': self.day_id,
            'hour': self.hour,
            'value': self.vslue
        }

    @classmethod
    def find_by_id(cls, item_id):
        hour = cls.query.filter_by(id=item_id).first()
        return hour

    @classmethod
    def find_by_day_id(cls, day_id):
        hour = cls.query.filter_by(day_id=day_id).all()

        #todo throw incomplete data event if hours are less than 24
        return hour

    def __repr__(self):
        return "<Hour id:'{}' hour:'{}' value:'{}'>".format(self.id, self.hour, self.value)
