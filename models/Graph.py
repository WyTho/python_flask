from datetime import date, datetime, timedelta, time

from db import db
from models import Week


class GraphModel(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    starting_date = None
    ending_date = None
    weeks = []

    def __init__(self, title, **kwargs):
        self.title = title
        if kwargs['starting_date']:
            self.starting_date_timestamp = kwargs['starting_date']
        if kwargs['ending_date']:
            self.ending_date_timestamp = kwargs['ending_date']

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'weeks': [week.to_json() for week in self.weeks]
        }

    @classmethod
    def find_all(cls):
        graphs = cls.query.all()
        for graph in graphs:
            weeks = []
            i = 0
            date_ = date.today() - timedelta(days=date.today().weekday())
            date_ = date_ - timedelta(weeks=6)
            date_ = datetime.combine(date_, datetime.min.time())
            while i < 7:
                weeks.append(Week.WeekModel(date_.timestamp(), graph.id))
                date_ = date_ + timedelta(weeks=1)
                i += 1
            graph.weeks = weeks
        return graphs

    @classmethod
    def find_by_title(cls, title, **kwargs):
        graph = cls.query.filter_by(title=title).first()

        if kwargs['starting_date_timestamp']:
            graph.starting_date = datetime.fromtimestamp(kwargs['starting_date_timestamp'])
            graph.ending_date = graph.starting_date + timedelta(weeks=6)
        elif kwargs['ending_date_timestamp']:
            graph.ending_date = datetime.fromtimestamp(kwargs['ending_date_timestamp'])
            graph.starting_date = graph.ending_date - timedelta(weeks=6)
        else:
            graph.ending_date = datetime.now()
            graph.starting_date = graph.ending_date - timedelta(weeks=6)

        i = 0
        weeks = []
        date_ = graph.starting_date
        while i < 7:
            weeks.append(Week.WeekModel(date_))
            date_ + timedelta(weeks=1)
            i += 1
        graph.weeks = weeks
        return graph

    def __repr__(self):
        return "<Graph id:'{}'>".format(self.id)
