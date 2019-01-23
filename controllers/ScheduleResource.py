from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from controllers.Validator import validate
import json
from datetime import datetime, time


class SchedulesResource(Resource):

    def get(self):
        all_schedules = ScheduleModel.find_all() or []
        all_in_json = [schedule.to_json() for schedule in all_schedules]
        return {"schedules": all_in_json}, 200

    def post(self):
        if 'time' in request.form.keys():
            schedule_time = request.form['time']
            if 'schedule_days' in request.form.keys():
                request_schedule_days = request.form['schedule_days']
            else:
                request_schedule_days = []
            if 'scheduled_usages' in request.form.keys():
                request_scheduled_usages = request.form['scheduled_usages']
            else:
                request_scheduled_usages = []
        else:
            request_data = json.loads(request.data)

            schedule_time = request_data['time']
            if 'schedule_days' in request_data.keys():
                request_schedule_days = request_data['schedule_days']
            else:
                request_schedule_days = []
            if 'scheduled_usages' in request_data.keys():
                request_scheduled_usages = request_data['scheduled_usages']
            else:
                request_scheduled_usages = []
        errors = validate(
            schedule_time=schedule_time,
            schedule_days=request_schedule_days,
            schedule_usages=request_scheduled_usages
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        schedule = ScheduleModel(datetime.strptime(schedule_time, "%H:%M:%S"))
        schedule.save_to_db()

        schedule_days = []
        for schedule_day in request_schedule_days:
            schedule_day = ScheduleDayModel(schedule.id, schedule_day)
            schedule_day.save_to_db()
            schedule_days.append(schedule_day)

        schedule.schedule_days = schedule_days

        scheduled_usages = []
        for scheduled_usage in request_scheduled_usages:
            scheduled_usage = ScheduledUsageModel(schedule.id, scheduled_usage['usage_id'], scheduled_usage['value'])
            scheduled_usage.save_to_db()
            scheduled_usages.append(scheduled_usage)
        schedule.scheduled_usages = scheduled_usages

        return schedule.to_json(), 201


class ScheduleResource(Resource):

    def get(self, schedule_id):
        errors = validate(schedule_id=schedule_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        schedule = ScheduleModel.find_by_id(schedule_id)
        return schedule.to_json()

    def put(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if 'time' in request.form.keys():
            schedule_time = request.form['time']
        else:
            request_data = json.loads(request.data)
            schedule_time = request_data['time']
        errors = validate(schedule_id=schedule_id, schedule_time=schedule_time)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        schedule.update(time)

    def delete(self, schedule_id):
        errors = validate(schedule_id=schedule_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        schedule = ScheduleModel.find_by_id(schedule_id)
        schedule.delete_from_db()
        return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
