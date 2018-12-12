from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from models.Usage import UsageModel
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
            if 'schedule_days' not in request.form:
                return 'No schedule days given.', 400
            request_schedule_days = request.form['schedule_days']
            if 'scheduled_usages' not in request.form:
                return 'No scheduled usages given.', 400
            request_scheduled_usages = request.form['scheduled_usages']
        else:
            request_data = json.loads(request.data)

            schedule_time = request_data['time']
            if 'schedule_days' not in request_data:
                return 'No schedule days given.', 400
            request_schedule_days = request_data['schedule_days']
            if 'scheduled_usages' not in request_data:
                return 'No scheduled usages given.', 400
            request_scheduled_usages = request_data['scheduled_usages']

        if len(schedule_time) != 8 or not datetime.strptime(schedule_time, "%H:%M:%S"):
            return 'Invalid time format given.', 400
        if len(request_schedule_days) < 1:
            return 'No schedule days given.', 400
        if len(request_scheduled_usages) < 1:
            return 'No scheduled usages given.', 400

        for schedule_day in request_schedule_days:
            schedule_day = int(schedule_day)
            if schedule_day < 0 or schedule_day > 6:
                return 'An incorrect value for day was given.', 400
        for scheduled_usage in request_scheduled_usages:
            if scheduled_usage['usage_id'] is None:
                return 'Missing Usage Id.', 400
            usage = UsageModel.find_by_id(scheduled_usage['usage_id'])
            if usage is None:
                return 'Could not find usage with id {}.'.format(scheduled_usage['usage_id']), 404
            if scheduled_usage['value'] < usage.min_value or scheduled_usage['value'] > usage.max_value:
                return 'Given usage value does not fall without range ({} - {}). ({} given.)' \
                    .format(usage.min_value, usage.max_value, scheduled_usage['value'])

        seen_values = []
        for schedule_day in request_schedule_days:
            if schedule_day in seen_values:
                return 'Duplicate day entry.', 400
            seen_values.append(schedule_day)

        seen_values = []
        for scheduled_usage in request_scheduled_usages:
            if scheduled_usage['usage_id'] in seen_values:
                return 'Duplicate usage entry.', 400
            seen_values.append(scheduled_usage['usage_id'])

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
        schedule = ScheduleModel.find_by_id(schedule_id)
        if schedule is None:
            return None, 404
        return schedule.to_json()

    def post(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if 'time' in request.form.keys():
            schedule_time = request.form['time']
        else:
            request_data = json.loads(request.data)
            schedule_time = request_data['time']

        if len(schedule_time) != 8 or not datetime.strptime(schedule_time, "%H:%M:%S"):
            return 'Invalid time format given.', 400
        schedule.update(time)

    def delete(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        schedule.delete_from_db()
        return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
