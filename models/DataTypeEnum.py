import enum
from db import db


class DataTypeEnum(enum.Enum):
    TEMPERATURE = 'TEMPERATURE'

    value = None

    def temperature(self):
        self.value = self.TEMPERATURE
        return self

    def is_temperature(self):
        return self.value == self.TEMPERATURE

t = db.Table(
    'data_type_enum', db.MetaData(),
    db.Column('value', db.Enum(DataTypeEnum))
)
