from db import db


class HourModel(db.Model):
    __tablename__ = 'hour'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=True)
    is_final_value = db.Column(db.Boolean, default=False)

    def __init__(self, day_id, hour, value, is_final_value):
        self.day_id = day_id
        self.hour = hour
        self.value = value
        self.is_final_value = is_final_value

    def to_json(self):
        return {
            'id': self.id,
            'day_id': self.day_id,
            'hour': self.hour,
            'value': self.value
        }

    @classmethod
    def find_by_id(cls, item_id):
        hour = cls.query.filter_by(id=item_id).first()
        return hour

    @classmethod
    def find_by_day_id(cls, day_id):
        hours = cls.query.filter_by(day_id=day_id).limit(24).all()
        return hours

    @classmethod
    def has_hour_with_day_id_and_hour(cls, day_id, hour):
        return cls.query.filter_by(day_id=day_id, hour=hour).first() is not None

    def update(self, value, is_final_value):
        self.value = value
        self.is_final_value = is_final_value
        db.session.commit()

    def save_to_db(self):
        print(self)
        db.session.add(self)
        db.session.commit()

    def has_value(self):
        return self.value is not None

    def __repr__(self):
        return "<Hour id:'{}' hour:'{}' value:'{}'>".format(self.id, self.hour, self.value)
