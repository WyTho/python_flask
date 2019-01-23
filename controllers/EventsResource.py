from flask_restful import Resource, request
from models.Event import EventModel
from models.Usage import UsageModel
from models.UnitEnum import UnitEnum
from models.Error import Error
from datetime import datetime
import json


class EventsResource(Resource):

    def get(self):
        all_events = EventModel.find_all() or []
        all_in_json = [event.to_json() for event in all_events]
        return {"events": all_in_json}, 200

    def post(self):
        errors = []
        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            data_type = request.form['data_type']
            data = request.form['data']
        else:
            request_data = json.loads(request.data)
            usage_id = request_data['usage_id']
            data_type = request_data['data_type']
            data = request_data['data']

        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            errors.append(Error(
                "Cannot find usage with id: {}".format(usage_id),
                "UsageModel.find_by_id({}) returns None".format(usage_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        if UnitEnum.has_value(data_type):
            data_type = UnitEnum(data_type)
        else:
            errors.append(Error(
                '"{}" is not a valid unit type.'.format(data_type),
                "UnitEnum.has_value({}) returned False".format(data_type), 400,
                "https://en.wikipedia.org/wiki/HTTP_400"
            ))

        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {"errors": all_errors_in_json}, 422

        if usage.unit != data_type:
            error = Error(
                'The unit type of the usage with id "{}" does not match the given "{}".'.format(usage_id, data_type),
                "usage.unit does not equal data_type.",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            )
            return {"errors": error.to_json()}, 422

        event = EventModel(usage_id, data, round(datetime.now().timestamp()))
        event.save_to_db()
        return event.to_json(), 201


class EventResource(Resource):

    def get(self, event_id):
        event = EventModel.find_by_id(event_id)
        return event.to_json()
