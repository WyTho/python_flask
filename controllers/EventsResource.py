from flask_restful import Resource, request
from models.Event import EventModel
import datetime


class EventsResource(Resource):

    def get(self):
        all = EventModel.find_all() or []
        all_in_json = [event.to_json() for event in all]
        return {"events": all_in_json}, 200

    def post(self):
        item_id = request.form['item_id']
        data_type = request.form['data_type']
        data = request.form['data']

        event = EventModel(item_id, data_type, data, datetime.datetime.timestamp(datetime.datetime.now()))
        event.save_to_db()
        return event.to_json(), 201


class EventResource(Resource):

    def get(self, event_id):
        event = EventModel.find_by_id(event_id)
        return event.to_json()
