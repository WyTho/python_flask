import enum
from db import db


class UsageTypeEnum(enum.Enum):
    KILOWATT = 'KILOWATT'
    WATER_PER_HOUR = 'WATER_PER_HOUR'
    WATER_PER_USAGE = 'WATER_PER_USAGE'

    value = None

    def create(self, usage_type):
        if usage_type == self.KILOWATT:
            self.value = self.KILOWATT
        elif usage_type == self.WATER_PER_HOUR:
            self.value = self.WATER_PER_HOUR
        elif usage_type == self.WATER_PER_USAGE:
            self.value = self.WATER_PER_USAGE
        else:
            raise ValueError('invalid value for UsageTypeEnum')

        return self

    def kilowatt(self):
        self.value = self.KILOWATT
        return self

    def is_kilowatt(self):
        return self.value == self.KILOWATT.value

    def water_per_hour(self):
        self.value = self.WATER_PER_HOUR
        return self

    def is_water_per_hour(self):
        return self.value == self.WATER_PER_HOUR.value

    def water_per_usage(self):
        self.value = self.WATER_PER_USAGE
        return self

    def is_water_per_usage(self):
        return self.value == self.WATER_PER_USAGE.value

t = db.Table(
    'usage_type_enum', db.MetaData(),
    db.Column('value', db.Enum(UsageTypeEnum))
)
