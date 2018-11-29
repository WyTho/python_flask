import enum
from db import db


class UnitEnum(enum.Enum):
    TOGGLE = 'TOGGLE'
    TEMPERATURE = 'TEMPERATURE'
    PERCENTAGE = 'PERCENTAGE'
    CUSTOM = 'CUSTOM'

    value = None

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def is_toggle(self):
        return self.value == self.TOGGLE

    def is_temperature(self):
        return self.value == self.TEMPERATURE

    def is_percentage(self):
        return self.value == self.PERCENTAGE

    def is_custom(self):
        return self.value == self.CUSTOM

t = db.Table(
    'unit_enum', db.MetaData(),
    db.Column('value', db.Enum(UnitEnum))
)
