from db import db
from .ScheduleDay import ScheduleDayModel
from .ScheduledUsage import ScheduledUsageModel
from datetime import time


class ScheduleModel(db.Model):
    __tablename__ = '_schedule'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    schedule_days = []
    scheduled_usages = []

    def __init__(self, time):
        self.time = time

    def to_json(self):
        return {
            'id': self.id,
            'time': self.time.strftime("%H:%M:%S"),
            'schedule_days': [schedule_day.to_json() for schedule_day in self.schedule_days],
            'scheduled_usages': [scheduled_usage.to_json() for scheduled_usage in self.scheduled_usages],
        }

    @classmethod
    def find_all(cls):
        schedules = cls.query.all()
        for schedule in schedules:
            schedule.schedule_days = ScheduleDayModel.find_by_schedule_id(schedule.id)
            schedule.scheduled_usages = ScheduledUsageModel.find_by_schedule_id(schedule.id)
        return schedules

    @classmethod
    def find_by_id(cls, schedule_id):
        schedule = cls.query.filter_by(id=schedule_id).first()
        if schedule is None:
            return None
        schedule.schedule_days = ScheduleDayModel.find_by_schedule_id(schedule_id)
        schedule.scheduled_usages = ScheduledUsageModel.find_by_schedule_id(schedule_id)
        return schedule

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self, time, list_with_day_numbers, list_with_scheduled_usages):
        self.time = time

        for schedule_day in self.schedule_days:
            if schedule_day.value not in list_with_day_numbers:
                schedule_day.delete_from_db()
        for day_number in list_with_day_numbers:
            if not self.has_day(day_number):
                ScheduleDayModel(self.id, day_number)

        for scheduled_usage in self.scheduled_usages:
            for new_scheduled_usage in list_with_scheduled_usages:
                pass

    def delete_from_db(self):
        schedule_days = ScheduleDayModel.find_by_schedule_id(self.id)
        for day in schedule_days:
            day.delete_from_db()

        scheduled_usages = ScheduledUsageModel.find_by_schedule_id(self.id)
        for usage in scheduled_usages:
            usage.delete_from_db()

        db.session.delete(self)
        db.session.commit()

    def has_day(self, day_number):
        for schedule_day in self.schedule_days:
            if schedule_day.day == day_number:
                return True
        return False

    def __repr__(self):
        return "<Schedule id:'{}'>".format(self.id)
