import threading
import time
from datetime import datetime, timedelta
from models.Day import DayModel
from models.Hour import HourModel


class RecalculateGraphValues(object):
    WATER_USAGE = 'WATER_USAGE'
    AVERAGE_TEMPERATURE = 'AVERAGE_TEMPERATURE'

    def __init__(self, graph):
        self.graph = graph

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        time.sleep(2)
        day = DayModel.find_by_id(1)
        print('{} FOUND #############################').format(day.id)

        # @todo actually do data science
        if self.graph.title == self.WATER_USAGE:
            print('Graphtype is {}'.format(self.WATER_USAGE))
        elif self.graph.title == self.AVERAGE_TEMPERATURE:
            print('Graphtype is {}'.format(self.AVERAGE_TEMPERATURE))
            self.check_for_missing_days(self.graph)
            self.check_for_missing_hours(self.graph)

    def check_for_missing_days(self, graph):
        for week in graph.weeks:
            if len(week.days) != 7:
                self.create_missing_days(week, graph.id)

    def create_missing_days(self, week, graph_id):
        starting_date = datetime.fromtimestamp(week.starting_date_timestamp)
        for day_of_week in range(0, 7):
            current_date_timestamp = (starting_date + timedelta(days=day_of_week)).timestamp()
            for day in week.days:
                if day.date_timestamp == current_date_timestamp:
                    break
            else:
                day_to_create = DayModel(graph_id, current_date_timestamp)
                day_to_create.save_to_db()

    def check_for_missing_hours(self, graph):
        for week in graph.weeks:
            for day in week.days:
                if len(day.hours) != 24:
                    self.create_missing_hours(day)

    def create_missing_hours(self, day):
        for hour in range(0, 24):
            if not HourModel.has_hour_with_day_id_and_hour(day.id, hour):
                print('creating new hour')