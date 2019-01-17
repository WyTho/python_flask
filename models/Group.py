from db import db
from . import ItemGroup
from flask import current_app as app
from models.Error import Error


class GroupModel(db.Model):
    __tablename__ = '_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_module = db.Column(db.Boolean, default=False)
    items = []

    def __init__(self, name, is_module):
        self.name = name
        self.is_module = is_module
        self.items = ItemGroup.ItemGroupModel.find_items_by_group_id(self.id)

    def to_json(self):
        if id is not None:
            url = "127.0.0.1:5000/api/groups/{}".format(self.id)
        else:
            url = "127.0.0.1:5000/api/groups/-1"
        return {
            'id': self.id,
            'name': self.name,
            'is_module': self.is_module,
            'items': [
                {
                    'id': item.id,
                    'name': item.name,
                    'comment': item.comment,
                    'url': '127.0.0.1:5000/api/items/{}'.format(item.id)
                } for item in self.items],
            # @todo during testing I cannot reach into app.config
            # 'url': app.config['API_URI'] + "groups/{}".format(self.id)
            'url': url
        }

    @classmethod
    def find_all(cls):
        groups = cls.query.all()
        for group in groups:
            group.items = ItemGroup.ItemGroupModel.find_items_by_group_id(group.id)
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

    def update_name(self, name):
        if len(name) < 3:
            return Error("Name must be at least 3 characters long.",
                         "Name parameter must be at least 3 characters long.",
                         400,
                         "https://en.wikipedia.org/wiki/HTTP_400")
        elif len(name) > 255:
            return Error("Name cannot be longer than 255 characters.",
                         "Name parameter cannot be longer than 255 characters.",
                         400,
                         "https://en.wikipedia.org/wiki/HTTP_400")
        self.name = name
        db.session.commit()
        return self

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
        return "<Group name:'{}'>".format(self.name)
