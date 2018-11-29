import enum
from db import db


class DataTypeEnum(enum.Enum):
    TEMPERATURE = 'TEMPERATURE'
    WATER_USAGE = 'WATER_USAGE'
    KILOWATT = 'KILOWATT'
    OTHER = 'OTHER'

    value = None

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def is_temperature(self):
        return self.value == self.TEMPERATURE

    def is_water_usage(self):
        return self.value == self.WATER_USAGE

    def is_kilowatt(self):
        return self.value == self.KILOWATT

    def is_other(self):
        return self.value == self.OTHER

t = db.Table(
    'data_type_enum', db.MetaData(),
    db.Column('value', db.Enum(DataTypeEnum))
)
