from db import db
from models.Usage import UsageModel


class ScheduledUsageModel(db.Model):
    __tablename__ = '_scheduled_usage'
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('_schedule.id'), nullable=False)
    usage_id = db.Column(db.Integer, db.ForeignKey('_usage.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, schedule_id, usage_id, value):
        self.schedule_id = schedule_id
        self.usage_id = usage_id
        self.value = value

    def to_json(self):
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'usage_id': self.usage_id,
            'value': self.value
        }

    def set_value(self, value):
        usage = UsageModel.find_by_id(self.usage_id)
        if value < usage.min_value or value > usage.max_value:
            return 'Given usage value does not fall without range ({} - {}). ({} given.)' \
                    .format(usage.min_value, usage.max_value, value), 500
        else:
            self.value = value
            return self.to_json(), 200

    @classmethod
    def find_all(cls):
        scheduled_usages = cls.query.all()
        return scheduled_usages

    @classmethod
    def find_by_schedule_id(cls, schedule_id):
        scheduled_usages = cls.query.filter_by(schedule_id=schedule_id).all()
        return scheduled_usages

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
        return "<Scheduled_usage id:'{}'>".format(self.id)
