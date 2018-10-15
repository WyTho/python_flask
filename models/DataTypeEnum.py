class DataTypeEnum:
    TEMPERATURE = 'TEMPERATURE'

    value = None

    def temperature(self):
        self.value = self.TEMPERATURE
        return self

    def is_temperature(self):
        return self.value == self.TEMPERATURE
