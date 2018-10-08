from flask_restful import Resource, request
from models.EventCall import EventCallModel


class EventCallsResource(Resource):

    def get(self):
        all = EventCallModel.find_all() or []
        all_in_json = [event.to_json() for event in all]
        return {"event_calls": all_in_json}, 200

    def post(self):
        event = EventCallModel(str(request.data))
        event.save_to_db()
        return event.to_json(), 201


class EventCallResource(Resource):

    def get(self, event_id):
        event = EventCallModel.find_by_id(event_id)
        return event.to_json()
