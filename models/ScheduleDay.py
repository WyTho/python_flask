from db import db


class ScheduleDayModel(db.Model):
    __tablename__ = '_schedule_day'
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('_schedule.id'), nullable=False)
    day = db.Column(db.Integer, nullable=False)

    def __init__(self, schedule_id, day):
        self.schedule_id = schedule_id
        self.day = day

    def to_json(self):
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'day': self.day
        }

    @classmethod
    def find_all(cls):
        schedule_days = cls.query.all()
        return schedule_days

    @classmethod
    def find_by_schedule_id(cls, schedule_id):
        schedule_days = cls.query.filter_by(schedule_id=schedule_id).all()
        return schedule_days

    @classmethod
    def find_by_schedule_id_and_day(cls, schedule_id, day):
        schedule_day = cls.query.filter_by(schedule_id=schedule_id).filter_by(day=day).first()
        return schedule_day

    @classmethod
    def find_by_id(cls, schedule_day_id):
        schedule_day = cls.query.filter_by(id=schedule_day_id).first()
        return schedule_day

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Schedule_day id:'{}'>".format(self.id)
