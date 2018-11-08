import enum
from db import db


class DataTypeEnum(enum.Enum):
    TEMPERATURE = 'TEMPERATURE'
    WATER_USAGE = 'WATER_USAGE'

    value = None

    def temperature(self):
        self.value = self.TEMPERATURE
        return self

    def is_temperature(self):
        return self.value == self.TEMPERATURE

    def water_usage(self):
        self.value = self.WATER_USAGE
        return self

    def is_water_usage(self):
        return self.value == self.WATER_USAGE

t = db.Table(
    'data_type_enum', db.MetaData(),
    db.Column('value', db.Enum(DataTypeEnum))
)
