from db import db


class ControlModel(db.Model):
    __tablename__ = 'control'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=True)
    max = db.Column(db.Integer, nullable=True)
    min = db.Column(db.Integer, nullable=True)

    def __init__(self, type, unit, max, min):
        self.type = type
        self.unit = unit
        self.max = max
        self.min = min

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'unit': self.unit,
            'min': self.min,
            'max': self.max
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, control_id):
        return cls.query.filter_by(id=control_id).first()

    @classmethod
    def filter(cls, **kwargs):

        results = cls.query
        if 'type' in kwargs:
            results = results.filter_by(type=kwargs['type'])
        if 'unit' in kwargs:
            results = results.filter_by(unit=kwargs['unit'])
        if 'max' in kwargs:
            results = results.filter_by(max=kwargs['max'])
        if 'min' in kwargs:
            results = results.filter_by(min=kwargs['min'])

        return results.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Control id:'{}', type:'{}', unit:'{}', min:'{}', max:'{}'>"\
            .format(self.id, self.type, self.unit, self.min, self.max)
