from db import db
from . import ItemGroup


class PlanningModel(db.Model):
    __tablename__ = '_planning'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    planning_days = []
    planned_usages = []

    def __init__(self, time):
        self.time = time

    def to_json(self):
        return {
            'id': self.id,
            'time': self.time,
            'planning_days': [day.to_json() for day in self.planning_days],
            'planned_usages': [planned_usage.to_json() for planned_usage in self.planned_usages],
        }

    @classmethod
    def find_all(cls):
        plannings = cls.query.all()
        for planning in plannings:
            planning.planning_days = PlanningDay.PlanningDayModel.find_by_planning_id(planning.id)
            
        return groups

    @classmethod
    def find_by_id(cls, group_id):
        group = cls.query.filter_by(id=group_id).first()
        if group is None:
            return None
        group.items = ItemGroup.ItemGroupModel.find_items_by_group_id(group.id)
        return group

    @classmethod
    def find_by_id_without_items(cls, group_id):
        return cls.query.filter_by(id=group_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        item_groups = ItemGroup.ItemGroupModel.find_by_group_id(self.id)
        for item_group in item_groups:
            item_group.delete_from_db()

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Planning name:'{}'>".format(self.name)
