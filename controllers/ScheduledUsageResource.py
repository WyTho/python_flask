from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from models.Usage import UsageModel
import json
import time


class ScheduledUsagesResource(Resource):

    def get(self, schedule_id):
        scheduled_usages = ScheduledUsageModel.find_by_schedule_id(schedule_id) or []
        all_in_json = [usage.to_json() for usage in scheduled_usages]
        return {"scheduled_usages": all_in_json}, 200

    def post(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if schedule is None:
            return 'Could not find schedule with id {}.'.format(schedule_id), 404

        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            value = request.form['value']
        else:
            request_data = json.loads(request.data)

            usage_id = request_data['usage_id']
            value = request_data['value']

        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            return 'Could not find usage with id {}.'.format(usage_id), 404

        for scheduled_usage in schedule.scheduled_usages:
            if scheduled_usage.usage_id == usage_id:
                return 'Given usage id is already being used by scheduled usage with id: {}.'\
                           .format(scheduled_usage.id), 500

        if value < usage.min_value or value > usage.max_value:
            return 'Given usage value does not fall without range ({} - {}). ({} given.)' \
                .format(usage.min_value, usage.max_value, value)

        scheduled_usage = ScheduledUsageModel(schedule.id, usage_id, value)

        return scheduled_usage.to_json(), 201


class ScheduledUsageResource(Resource):

    def get(self, schedule_id, scheduled_usage_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if schedule is None:
            return "Could not find schedule with id {}.".format(schedule_id)

        scheduled_usage = schedule.find_scheduled_usage_by_id(scheduled_usage_id)
        if scheduled_usage is None:
            return "Could not find scheduled usage with id {} on schedule with id {}."\
                   .format(scheduled_usage_id, schedule_id), 404
        return scheduled_usage.to_json(), 200

    def post(self, schedule_id, scheduled_usage_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if 'value' in request.form.keys():
            value = request.form['value']
        else:
            request_data = json.loads(request.data)
            value = request_data['value']

        if schedule is None:
            return "Could not find schedule with id {}.".format(schedule_id)

        scheduled_usage = schedule.find_scheduled_usage_by_id(scheduled_usage_id)
        if scheduled_usage is None:
            return "Could not find scheduled usage with id {} on schedule with id {}."\
                   .format(scheduled_usage_id, schedule_id), 404

        return scheduled_usage.set_value(value)

    def delete(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        schedule.delete_from_db()
        return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
