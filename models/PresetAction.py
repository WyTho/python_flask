from db import db


class PresetActionModel(db.Model):
    __tablename__ = '_preset_action'
    id = db.Column(db.Integer, primary_key=True)
    preset_id = db.Column(db.Integer, db.ForeignKey('_preset.id'))
    usage_id = db.Column(db.Integer, db.ForeignKey('_usage.id'))
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, preset_id, usage_id, value):
        self.preset_id = preset_id
        self.usage_id = usage_id
        self.value = value

    def to_json(self):
        return {
            'id': self.id,
            'preset_id': self.preset_id,
            'usage_id': self.usage_id,
            'value': self.value
        }

    @classmethod
    def find_all(cls):
        preset_actions = cls.query.all()
        return preset_actions

    @classmethod
    def find_preset_actions_by_preset_id(cls, preset_id):
        preset_actions = cls.query.filter_by(preset_id=preset_id).all()
        return preset_actions

    @classmethod
    def find_by_id(cls, preset_action_id):
        preset = cls.query.filter_by(id=preset_action_id).first()
        return preset

    def update(self, usage_id, value):
        self.usage_id = usage_id
        self.value = value

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Preset_action id:'{}'>".format(self.id)
