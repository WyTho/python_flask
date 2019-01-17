from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from controllers.Validator import validate
import json


class ScheduleDaysResource(Resource):

    def get(self, schedule_id):
        errors = validate(schedule_id=schedule_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        schedule_days = ScheduleDayModel.find_by_schedule_id(schedule_id) or []
        all_in_json = [day.to_json() for day in schedule_days]
        return {"schedule_days": all_in_json}, 200

    def post(self, schedule_id):
        if 'day' in request.form.keys():
            day = int(request.form['day'])
        else:
            request_data = json.loads(request.data)
            day = int(request_data['day'])

        errors = validate(schedule_id=schedule_id, schedule_day_number=day)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404

        schedule_day = ScheduleDayModel(schedule_id, day)
        return schedule_day.to_json(), 201


class ScheduleDayResource(Resource):

    def delete(self, schedule_id, schedule_day_id):
        errors = validate(schedule_id=schedule_id, schedule_day_id=schedule_day_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        schedule_day = ScheduleDayModel.find_by_id(schedule_day_id)
        schedule_day.delete_from_db()

        return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
