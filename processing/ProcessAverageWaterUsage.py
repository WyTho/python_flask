from models.Event import EventModel
from models.Day import DayModel
from models.DataTypeEnum import DataTypeEnum
from datetime import datetime, timedelta
from models.Usage import UsageModel


class AverageWaterUsageProcessor:

    def process_hour_value(self, hour):
        day = DayModel.find_by_id(hour.day_id)
        after_datetime = (datetime.fromtimestamp(day.date_timestamp) + timedelta(hours=hour.hour))
        before_datetime = (datetime.fromtimestamp(day.date_timestamp) + timedelta(hours=hour.hour + 1))
        events = EventModel.filter(data_type=DataTypeEnum.WATER_USAGE.value,
                                   after_timestamp=after_datetime.timestamp(),
                                   before_timestamp=before_datetime.timestamp())
        total_water_usage = 0
        for event in events:
            usage = UsageModel.find_by_id(event.usage_id)
            if usage.usage_type.is_water_per_hour():
                if event.data == 'True':
                    # @todo: This now ignores the fact that a usage can be spread out over multiple hours and
                    # just adds it to the hour at wich the usage was initiated
                    start = event.timestamp
                    end = EventModel.find_next_false(event).timestamp

                    duration_in_seconds = end - start
                    duration_in_hours = duration_in_seconds / (60 * 60)
                    total_water_usage += duration_in_hours * int(usage.usage)

            elif usage.usage_type.is_water_per_usage():
                total_water_usage += int(usage.usage)

        # is_final_value = before_datetime.timestamp() < datetime.now().timestamp()
        is_final_value = False
        hour.update(total_water_usage, is_final_value)