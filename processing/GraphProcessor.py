from models.Hour import HourModel
from models.Day import DayModel
from models.Graph import GraphModel
from datetime import timedelta, datetime
from processing.ProcessAverageTemperature import AverageTemperatureProcessor


class GraphProcessor:
    graph = None

    def __init__(self, graph):
        self.graph = graph

    def process(self):
        print('in processor')
        self.complete_graph()

        processor = None
        # @todo add graph type (might be on real_PC)
        if self.graph.title == 'AVERAGE_TEMPERATURE':
            processor = AverageTemperatureProcessor()

        for week in self.graph.weeks:
            for day in week.days:
                for hour in day.hours:
                    if not hour.is_final_value:
                        processor.process_hour_value(hour)

        return GraphModel.find_by_title(self.graph.title)

    def create_hours(self, day):
        missing_hours = []
        for i in range(0, 24):
            hour_found = False
            for hour in day.hours:
                if hour.hour == i:
                    hour_found = True
            if not hour_found:
                missing_hours.append(i)

        for missing_hour in missing_hours:
            # @todo remove hour not null constraint when both versions are pushed. Hours that lie into the
            # future have to value after all
            hour = HourModel(day.id, missing_hour, 0.0, False)
            hour.save_to_db()
            day.add_hour(hour)

    def create_days(self, week):
        missing_days = []
        date_timestamp = week.starting_date_timestamp
        for i in range(0, 7):
            for day in week.days:
                if datetime.fromtimestamp(day.date_timestmap) == (datetime.fromtimestamp(date_timestamp) + timedelta(days=i)):
                    break
            missing_days.append(datetime.fromtimestamp(week.starting_date_timestamp) + timedelta(days=i))

        for missing_day in missing_days:
            day = DayModel(self.graph.id, missing_day.timestamp())
            day.save_to_db()
            week.add_day(day)

    def complete_graph(self):
        for week in self.graph.weeks:
            if not week.has_7_days():
                print('creating_days')
                self.create_days(week)

        for week in self.graph.weeks:
            for day in week.days:
                if not day.has_24_hours():
                    self.create_hours(day)
