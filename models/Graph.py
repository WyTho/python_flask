from datetime import date, datetime, timedelta, time
from db import db
from models import Week
from models.DataTypeEnum import DataTypeEnum


class GraphModel(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    data_type = db.Column(db.Enum(DataTypeEnum))
    starting_date = None
    ending_date = None
    weeks = []

    def __init__(self, title, data_type_enum, **kwargs):
        self.title = title
        self.data_type = data_type_enum
        if kwargs['starting_date']:
            self.set_starting_date(kwargs['starting_date'])
        if kwargs['ending_date']:
            self.set_ending_date(kwargs['ending_date'])

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'data_type': self.data_type.value,
            'weeks': [week.to_json() for week in self.weeks]
        }

    @classmethod
    def find_all_types(cls):
        graphs = cls.query.all()
        types = []
        for graph in graphs:
            types.append(graph.title)
        return types

    @classmethod
    def find_all(cls):
        graphs = cls.query.all()
        for graph in graphs:
            weeks = []
            i = 0
            first_day_of_current_week = date.today() - timedelta(days=date.today().weekday())
            first_day_of_graph = first_day_of_current_week - timedelta(weeks=6)
            first_day_of_graph = datetime.combine(first_day_of_graph, datetime.min.time())
            graph.set_starting_date(first_day_of_graph)
            date_ = first_day_of_graph
            while i < 7:
                weeks.append(Week.WeekModel(date_.timestamp(), graph.id))
                date_ = date_ + timedelta(weeks=1)
                i += 1
            graph.set_weeks(weeks)
        return graphs

    @classmethod
    def find_by_title(cls, title, **kwargs):
        graph = cls.query.filter_by(title=title).first()

        starting_date_timestamp = None
        ending_date_timestamp = None
        if 'starting_date_timestamp' in kwargs:
            starting_date_timestamp = kwargs['starting_date_timestamp']
        if 'ending_date_timestamp' in kwargs:
            ending_date_timestamp = kwargs['ending_date_timestamp']

        # @todo test while using params
        if starting_date_timestamp is not None:
            graph.set_starting_date(datetime.fromtimestamp(starting_date_timestamp))
            graph.set_ending_date(graph.starting_date + timedelta(weeks=6))
        elif ending_date_timestamp is not None:
            graph.set_ending_date(datetime.fromtimestamp(ending_date_timestamp))
            graph.set_starting_date(graph.ending_date - timedelta(weeks=6))
        else:
            last_day_of_current_week = date.today() + timedelta(days=(7 - date.today().weekday()))
            graph.set_ending_date(datetime.combine(last_day_of_current_week, datetime.min.time()))
            graph.set_starting_date(graph.ending_date - timedelta(weeks=6))

        i = 0
        weeks = []
        date_ = graph.starting_date
        while i < 6:
            weeks.append(Week.WeekModel(date_.timestamp(), graph.id))
            date_ = date_ + timedelta(weeks=1)
            i += 1
        graph.set_weeks(weeks)
        return graph

    def set_weeks(self, weeks):
        self.weeks = weeks

    def set_starting_date(self, starting_date):
        self.starting_date = starting_date

    def set_ending_date(self, ending_date):
        self.ending_date = ending_date

    def __repr__(self):
        return "<Graph id:'{}'>".format(self.id)
