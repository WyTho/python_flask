from db import db
from models.PresetAction import PresetActionModel


class PresetModel(db.Model):
    __tablename__ = '_preset'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('_group.id'))
    name = db.Column(db.String(30), nullable=False)
    preset_actions = []

    def __init__(self, group_id, name):
        self.name = name
        self.group_id = group_id
        self.preset_actions = PresetActionModel.find_preset_actions_by_preset_id(self.id)

    def to_json(self):
        if self.id is not None:
            url = "127.0.0.1:5000/api/v1/groups/{}/presets/{}".format(self.group_id, self.id)
        else:
            url = "127.0.0.1:5000/api/v1/groups/{}/presets/-1".format(self.group_id)
        return {
            'id': self.id,
            'group_id': self.group_id,
            'name': self.name,
            'preset_actions': [
                preset_action.to_json() for preset_action in self.preset_actions],
            'url': url
        }

    @classmethod
    def find_all(cls):
        presets = cls.query.all()
        for preset in presets:
            preset.preset_actions = PresetActionModel.find_preset_actions_by_preset_id(preset.id)
        return presets

    @classmethod
    def find_all_by_group_id(cls, group_id):
        presets = cls.query.filter_by(group_id=group_id).all()
        for preset in presets:
            preset.preset_actions = PresetActionModel.find_preset_actions_by_preset_id(preset.id)
        return presets

    @classmethod
    def find_by_id(cls, preset_id):
        preset = cls.query.filter_by(id=preset_id).first()
        if preset is None:
            return None
        preset.preset_actions = PresetActionModel.find_preset_actions_by_preset_id(preset.id)
        return preset

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        for preset_action in self.preset_actions:
            preset_action.delete_from_db()

        db.session.delete(self)
        db.session.commit()

    def set_name(self, name):
        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 30:
            return 'Name cannot be longer than 30 characters.', 400
        self.name = name
        db.session.commit()
        return self

    def __repr__(self):
        return "<Preset name:'{}'>".format(self.name)
