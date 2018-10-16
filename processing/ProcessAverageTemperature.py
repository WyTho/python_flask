from models.Event import EventModel
from models.Day import DayModel
from models.DataTypeEnum import DataTypeEnum
from datetime import datetime, timedelta


class AverageTemperatureProcessor:

    def process_hour_value(self, hour):
        day = DayModel.find_by_id(hour.day_id)
        after_datetime = (datetime.fromtimestamp(day.date_timestamp) + timedelta(hours=hour.hour))
        before_datetime = (datetime.fromtimestamp(day.date_timestamp) + timedelta(hours=hour.hour + 1))
        events = EventModel.filter(data_type=DataTypeEnum.TEMPERATURE.value,
                                   after_timestamp=after_datetime.timestamp(),
                                   before_timestamp=before_datetime.timestamp())

        temperature_sum = 0
        for event in events:
            temperature_sum += float(event.data)
        if temperature_sum == 0:
            value = 0
        else:
            value = temperature_sum / len(events)

        is_final_value = before_datetime.timestamp() < datetime.now().timestamp()
        hour.update(value, is_final_value)
        print('updated hour: ')
        print(hour)
