from flask_restful import Resource, request
from models.Event import EventModel
from models.Usage import UsageModel
from models.DataTypeEnum import DataTypeEnum
from datetime import datetime
import json


class EventsResource(Resource):

    def get(self):
        all_events = EventModel.find_all() or []
        all_in_json = [event.to_json() for event in all_events]
        return {"events": all_in_json}, 200

    def post(self):
        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            data_type = request.form['data_type']
            data = request.form['data']
        else:
            request_data = json.loads(request.data)
            usage_id = request_data['usage_id']
            data_type = request_data['data_type']
            data = request_data['data']

        if UsageModel.find_by_id(usage_id) is None:
            return 'Could not find usage with id: {}'.format(usage_id), 404
        if DataTypeEnum.has_value(data_type):
            data_type = DataTypeEnum(data_type)
        else:
            return '"{}" is not a valid data type.'.format(data_type), 400

        event = EventModel(usage_id, data_type, data, round(datetime.now().timestamp()))
        event.save_to_db()
        return event.to_json(), 201


class EventResource(Resource):

    def get(self, event_id):
        event = EventModel.find_by_id(event_id)
        return event.to_json()
