from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from models.Usage import UsageModel
import json
import time


class SchedulesResource(Resource):

    def get(self):
        all_schedules = ScheduleModel.find_all() or []
        all_in_json = [schedule.to_json() for schedule in all_schedules]
        return {"schedules": all_in_json}, 200

    def post(self):
        if 'time' in request.form.keys():
            schedule_time = request.form['time']
            request_schedule_days = request.form['schedule_days']
            request_scheduled_usages = request.form['scheduled_usages']
        else:
            request_data = json.loads(request.data)

            schedule_time = request_data['time']
            request_schedule_days = request_data['schedule_days']
            request_scheduled_usages = request_data['scheduled_usages']

        if len(schedule_time) != 8 or not time.strptime(schedule_time, "%H:%M:%S"):
            return 'Invalid time format given.', 400
        if request_schedule_days is None:
            return 'No schedule days given.', 400
        if len(request_schedule_days) < 1:
            return 'No schedule days given.', 400
        if request_scheduled_usages is None:
            return 'No scheduled usages given.', 400
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

        schedule = ScheduleModel(schedule_time)
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
            list_with_day_numbers = request.form['schedule_days']
            list_with_scheduled_usages = request.form['scheduled_usages']
        else:
            request_data = json.loads(request.data)

            schedule_time = request_data['time']
            list_with_day_numbers = request_data['schedule_days']
            list_with_scheduled_usages = request_data['scheduled_usages']

        if len(schedule_time) != 8 or not time.strptime(schedule_time, "%H:%M:%S"):
            return 'Invalid time format given.', 400
        if list_with_day_numbers is None:
            return 'No schedule days given.', 400
        if len(list_with_day_numbers) < 1:
            return 'No schedule days given.', 400
        if list_with_scheduled_usages is None:
            return 'No scheduled usages given.', 400
        if len(list_with_scheduled_usages) < 1:
            return 'No scheduled usages given.', 400

        for schedule_day in list_with_day_numbers:
            schedule_day = int(schedule_day)
            if schedule_day < 0 or schedule_day > 6:
                return 'An incorrect value for day was given.', 400
        for scheduled_usage in list_with_scheduled_usages:
            if scheduled_usage['usage_id'] is None:
                return 'Missing Usage Id.', 400
            usage = UsageModel.find_by_id(scheduled_usage['usage_id'])
            if usage is None:
                return 'Could not find usage with id {}.'.format(scheduled_usage['usage_id']), 404
            if scheduled_usage['value'] < usage.min_value or scheduled_usage['value'] > usage.max_value:
                return 'Given usage value does not fall without range ({} - {}). ({} given.)' \
                    .format(usage.min_value, usage.max_value, scheduled_usage['value'])

        schedule.update(time, list_with_day_numbers, list_with_scheduled_usages)
    # def post(self, item_id):
    #     item = ItemModel.find_by_id(item_id)
    #     if 'name' in request.form.keys():
    #         name = request.form['name']
    #         comment = request.form['comment']
    #     else:
    #         request_data = json.loads(request.data)
    #         name = request_data['name']
    #         comment = request_data['comment']
    #
    #     if len(name) < 3:
    #         return 'Name must be at least 3 characters long.', 400
    #     if len(name) > 255:
    #         return 'Name cannot be longer than 255 characters.', 400
    #     if len(comment) > 255:
    #         return 'Comment cannot be longer than 255 characters.', 400
    #
    #     item = item.update(name=name, comment=comment)
    #     return item.to_json()

    def delete(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        schedule.delete_from_db()
        return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
