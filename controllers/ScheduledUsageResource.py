from flask_restful import Resource, request
from models.ScheduledUsage import ScheduledUsageModel
from controllers.Validator import validate
import json


class ScheduledUsagesResource(Resource):

    def get(self, schedule_id):
        scheduled_usages = ScheduledUsageModel.find_by_schedule_id(schedule_id) or []
        all_in_json = [usage.to_json() for usage in scheduled_usages]
        return {"scheduled_usages": all_in_json}, 200

    def post(self, schedule_id):

        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            value = request.form['value']
        else:
            request_data = json.loads(request.data)

            usage_id = request_data['usage_id']
            value = request_data['value']
        validate(
            schedule_id=schedule_id,
            usage_id=usage_id,
            usage_value=value,
            method="ScheduledUsagesResource.post"
        )

        scheduled_usage = ScheduledUsageModel(schedule_id, usage_id, value)
        return scheduled_usage.to_json(), 201


class ScheduledUsageResource(Resource):

    def get(self, schedule_id, scheduled_usage_id):
        errors = validate(schedule_id=schedule_id, scheduled_usage_id=scheduled_usage_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        scheduled_usage = ScheduledUsageModel.find_by_id(scheduled_usage_id)
        return scheduled_usage.to_json(), 200

    def put(self, schedule_id, scheduled_usage_id):
        if 'value' in request.form.keys():
            value = request.form['value']
        else:
            request_data = json.loads(request.data)
            value = request_data['value']
        errors = validate(schedule_id=schedule_id, scheduled_usage_id=scheduled_usage_id, scheduled_usage_value=value)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}

        scheduled_usage = ScheduledUsageModel.find_by_id(scheduled_usage_id)
        return scheduled_usage.set_value(value).to_json(), 200

    def delete(self, schedule_id, scheduled_usage_id):
        errors = validate(schedule_id=schedule_id, scheduled_usage_id=scheduled_usage_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}

        scheduled_usage = ScheduledUsageModel.find_by_id(scheduled_usage_id)
        scheduled_usage.delete_from_db()
        return "Schedule Usage with id: {} was successfully deleted.".format(scheduled_usage_id), 200
