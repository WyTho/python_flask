import enum
from db import db


class UsageTypeEnum(enum.Enum):
    KILOWATT = 'KILOWATT'
    WATER_PER_HOUR = 'WATER_PER_HOUR'
    WATER_PER_USAGE = 'WATER_PER_USAGE'

    value = None

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def is_kilowatt(self):
        return self.value == self.KILOWATT.value

    def is_water_per_hour(self):
        return self.value == self.WATER_PER_HOUR.value

    def is_water_per_usage(self):
        return self.value == self.WATER_PER_USAGE.value

t = db.Table(
    'usage_type_enum', db.MetaData(),
    db.Column('value', db.Enum(UsageTypeEnum))
)
