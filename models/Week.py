from datetime import timedelta, datetime
from models import Day


class WeekModel():
    starting_date_timestamp = None
    graph_id = -1
    days = []

    def __init__(self, date_timestamp, graph_id):
        date_ = datetime.fromtimestamp(date_timestamp)
        starting_date = date_ - timedelta(days=date_.weekday())
        self.starting_date_timestamp = starting_date

        days = []
        date_ = starting_date
        i = 0
        while i < 7:
            days.append(Day.DayModel.find_by_date_and_graph_id(date_.timestamp(), graph_id))
            date_ = date_ + timedelta(days=1)
            i += 1

        self.days = days

    def to_json(self):
        return {
            'days': [day.to_json() for day in self.days]
        }