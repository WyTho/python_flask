from flask_restful import Resource, request
from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from models.Usage import UsageModel
import json
import time


class ScheduleDaysResource(Resource):

    def get(self, schedule_id):
        schedule_days = ScheduleDayModel.find_by_schedule_id(schedule_id) or []
        all_in_json = [day.to_json() for day in schedule_days]
        return {"schedule_days": all_in_json}, 200

    def post(self, schedule_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        if schedule is None:
            return 'Could not find schedule with id {}.'.format(schedule_id), 404

        if 'day' in request.form.keys():
            day = int(request.form['day'])
        else:
            request_data = json.loads(request.data)
            day = int(request_data['day'])

        for schedule_day in schedule.schedule_days:
            if schedule_day.day == day:
                return 'Given day ({}) is already being used.'\
                           .format(day), 400

        schedule_day = ScheduleDayModel(schedule.id, day)

        return schedule_day.to_json(), 201


class ScheduleDayResource(Resource):

    def delete(self, schedule_id, schedule_day_id):
        schedule = ScheduleModel.find_by_id(schedule_id)
        schedule_day = ScheduleDayModel.find_by_id(schedule_day_id)
        if schedule.id == schedule_day.schedule_id:
            schedule_day.delete_from_db()
            return "Schedule with id: {} was successfully deleted.".format(schedule_id), 200
        else:
            return "The given schedule id does not match the schedule id of schedule day with id {}."\
                .format(schedule_day_id)
