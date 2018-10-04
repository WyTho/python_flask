from db import db
from . import Event


class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    events = []

    def __init__(self, name, address, comment):
        self.name = name
        self.address = address
        self.comment = comment
        self.events = Event.EventModel.find_all_by_item_id(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'comment': self.comment,
            'events': [event.to_json() for event in self.events]
        }

    @classmethod
    def find_all(cls):
        items = cls.query.all()
        for item in items:
            item.events = Event.EventModel.find_all_by_item_id(item.id)
        return items

    @classmethod
    def find_by_id(cls, item_id):
        item = cls.query.filter_by(id=item_id).first()
        item.events = Event.EventModel.find_all_by_item_id(item.id)
        return item

    def update(self, **kwargs):
        if kwargs['name']:
            self.name = kwargs['name']
        if kwargs['address']:
            self.address = kwargs['address']
        if kwargs['comment']:
            self.comment = kwargs['comment']

        db.session.commit()
        return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Item name:'{}', address:'{}', comment:'{}'>".format(self.name, self.address, self.comment)
