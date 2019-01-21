from models.Item import ItemModel
from models.Usage import UsageModel
from models.Group import GroupModel
from models.Preset import PresetModel
from models.PresetAction import PresetActionModel
from models.Schedule import ScheduleModel
from models.ScheduledUsage import ScheduledUsageModel
from models.ScheduleDay import ScheduleDayModel
from models.Error import Error
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum
from datetime import datetime


def validate(**kwargs):
    errors = []
    item = None
    usage = None
    group = None
    preset = None
    schedule = None
    scheduled_usage = None
    method = None
    if "method" in kwargs:
        method = kwargs.pop('method')

    # ITEM
    if "item_id" in kwargs:
        item_id = kwargs.pop("item_id")
        item = ItemModel.find_by_id(item_id)
        if item is None:
            errors.append(Error(
                "Could not find item with id: {}".format(item_id),
                "ItemMode.find_by_id({}) returned None".format(item_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
    if "item_name" in kwargs:
        item_name = kwargs.pop("item_name")
        if len(item_name) < 3:
            errors.append(Error(
                "Name must be at least 3 characters long.",
                "Name parameter must be at least 3 characters long.",
                400,
                "https://en.wikipedia.org/wiki/HTTP_400"))
        elif len(item_name) > 255:
            errors.append(Error(
                "Name cannot be longer than 255 characters.",
                "Name parameter cannot be longer than 255 characters.",
                400,
                "https://en.wikipedia.org/wiki/HTTP_400"))
    if "item_comment" in kwargs:
        item_comment = kwargs.pop('item_comment')
        if len(item_comment) > 255:
            errors.append(Error(
                "Comment cannot be longer than 255 characters.",
                "Name parameter cannot be longer than 255 characters.",
                400,
                "https://en.wikipedia.org/wiki/HTTP_400"))

    # USAGE
    if "usage_id" in kwargs:
        usage_id = kwargs.pop('usage_id')
        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            errors.append(Error(
                "Could not find usage with id: {}".format(usage_id),
                "UsageModel.find_by_id({}) returned None".format(usage_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        elif item is not None:
            if not item.has_usage(usage_id):
                errors.append(Error(
                    "Item with id {} does not have usage with id: {}".format(item.id, usage_id),
                    "UsageModel.find_by_id({}) returned None".format(usage_id),
                    404,
                    "https://en.wikipedia.org/wiki/HTTP_404"))

    if "usage_value" in kwargs:
        usage_value = kwargs.pop("usage_value")
        if usage is None:
            pass
        elif usage_value < usage.min_value or usage_value > usage.max_value:
            errors.append(Error(
                "Given value is not in range of Usage values. ({} - {}) ({} given)".format(
                    usage.min_value, usage.max_value, usage_value),
                "value is not within range. ({} - {}) ({} given)".format(
                    usage.min_value, usage.max_value, usage_value),
                422,
                "https://en.wikipedia.org/wiki/HTTP_404"
            ))
    if "usage_consumption_type" in kwargs:
        usage_consumption_type = kwargs.pop('usage_consumption_type')
        if not UsageTypeEnum.has_value(usage_consumption_type):
            errors.append(Error(
                "{} is not a valid consumption type.".format(usage_consumption_type),
                "UsageTypeEnum.has_value({}) returned False".format(usage_consumption_type),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
    if "usage_unit" in kwargs:
        usage_unit = kwargs.pop('usage_unit')
        if not UnitEnum.has_value(usage_unit):
            errors.append(Error(
                "{} is not a valid unit option.".format(usage_unit),
                "UnitEnum.has_value({}) returned False".format(usage_unit),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
    if "usage_address" in kwargs:
        usage_address = kwargs.pop('usage_address')
        if len(usage_address) < 3:
            errors.append(Error(
                "Address must be at least 4 characters long.",
                "address was {} characters long".format(len(usage_address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if len(usage_address) > 255:
            errors.append(Error(
                "Address cannot be longer than 255 characters.",
                "address was {} characters long".format(len(usage_address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
    if "usage_consumption_amount" in kwargs:
        usage_consumption_amount = kwargs.pop("usage_consumption_amount")
        if usage_consumption_amount < 0:
            errors.append(Error(
                "Consumption amount cannot be below 0.",
                "{} is below 0".format(usage_consumption_amount),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
    usage_min_value = None
    if "usage_min_value" in kwargs:
        usage_min_value = kwargs.pop("usage_min_value")
    usage_max_value = None
    if "usage_max_value" in kwargs:
        usage_max_value = kwargs.pop("usage_max_value")
    if (usage_min_value is None and usage_max_value is not None) or \
            (usage_min_value is not None and usage_max_value is None):
        errors.append(Error(
            "If either min or max value is given, both should be given.",
            "Either min or max was None while the other was not.",
            422,
            "https://en.wikipedia.org/wiki/HTTP_422"))
    elif usage_min_value is not None and usage_max_value is not None:
        if usage_min_value > usage_max_value:
            errors.append(Error(
                "Min value should be lower than max value",
                "min_value is higher than max_value",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))

    # GROUP
    if "group_id" in kwargs:
        group_id = kwargs.pop("group_id")
        group = GroupModel.find_by_id(group_id)
        if group is None:
            errors.append(Error(
                "Could not find group with id: {}".format(group_id),
                "GroupModel.find_by_id({}) returned None".format(group_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))

    if "group_name" in kwargs:
        group_name = kwargs.pop("group_name")
        if len(group_name) < 3:
            errors.append(Error(
                "Name must be at least 3 characters long.",
                "Name parameter must be at least 3 characters long.",
                400,
                "https://en.wikipedia.org/wiki/HTTP_400"))
        elif len(group_name) > 255:
            errors.append(Error(
                "Name cannot be longer than 255 characters.",
                "Name parameter cannot be longer than 255 characters.",
                400,
                "https://en.wikipedia.org/wiki/HTTP_400"))

    # PRESET
    if "preset_id" in kwargs:
        preset_id = kwargs.pop("preset_id")
        preset = PresetModel.find_by_id(preset_id)
        if preset is None:
            errors.append(Error(
                "Could not find preset with id: {}".format(preset_id),
                "PresetModel.find_by_id({}) returned None".format(preset_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        elif preset.group_id != group.id:
            errors.append(Error(
                "The given group id did not match the presets group id",
                "preset.group_id != group.id",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))

    if "preset_name" in kwargs:
        preset_name = kwargs.pop("preset_name")
        if len(preset_name) < 3:
            errors.append(Error(
                "Name must be at least 3 characters long.",
                "len(preset_name) < 3 returned True",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
        if len(preset_name) > 30:
            errors.append(Error(
                "Name cannot be longer than 30 characters.",
                "len(preset_name) > 30 returned True",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))

    # PRESET_ACTION
    if "preset_action_id" in kwargs:
        preset_action_id = kwargs.pop("preset_action_id")
        preset_action = PresetActionModel.find_by_id(preset_action_id)
        if preset_action is None:
            errors.append(Error(
                "Could not find preset action with id: {}".format(preset_action_id),
                "PresetActionModel.find_by_id({}) returned None".format(preset_action_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        elif preset is not None:
            if preset_action.preset_id != preset.id:
                errors.append(Error(
                    "The given preset id did not match the presets actions preset id",
                    "preset_action.preset_id != preset.id",
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_422"
            ))

    # SCHEDULE
    if "schedule_id" in kwargs:
        schedule_id = kwargs.pop("schedule_id")
        schedule = ScheduleModel.find_by_id(schedule_id)
        if schedule is None:
            errors.append(Error(
                "Could not find schedule with id: ".format(schedule_id),
                "ScheduleModel.find_by_id({}) returned None".format(schedule_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
    if "schedule_time" in kwargs:
        schedule_time = kwargs.pop("schedule_time")
        if len(schedule_time) != 8 or not datetime.strptime(schedule_time, "%H:%M:%S"):
            errors.append(Error(
                "Invalid time format given, expected format is: '12:00:00'",
                "Invalid time format, expected format is: '%H:%M:%S'",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
    if "schedule_days" in kwargs:
        schedule_days = kwargs.pop("schedule_days")
        if len(schedule_days) < 1:
            errors.append(Error(
                "No schedule days given.",
                "Expecting array of days",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
        else:
            seen_values = []
            for schedule_day in schedule_days:
                if int(schedule_day) < 0 or int(schedule_day) > 6:
                    errors.append(Error(
                        "day should be in range 0 - 6, {} given".format(int(schedule_day)),
                        "day should be in range 0 - 6, {} given".format(int(schedule_day)),
                        422,
                        "https://en.wikipedia.org/wiki/HTTP_422"
                    ))
                if schedule_day in seen_values:
                    errors.append(Error(
                        "Duplicate day entry. {}".format(schedule_day),
                        "Duplicate day entry. {}".format(schedule_day),
                        422,
                        "https://en.wikipedia.org/wiki/HTTP_422"
                    ))
                seen_values.append(schedule_day)
    if "schedule_usages" in kwargs:
        schedule_usages = kwargs.pop("schedule_usages")
        if len(schedule_usages) < 1:
            errors.append(Error(
                "No schedule usages given.",
                "Expecting array of usages",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
        seen_values = []
        for scheduled_usage in schedule_usages:
            if scheduled_usage['usage_id'] is None:
                errors.append(Error(
                    "Missing usage_id for a scheduled usage.",
                    "Missing usage_id for a scheduled usage.",
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_422"
                ))
            else:
                _usage = UsageModel.find_by_id(scheduled_usage['usage_id'])
                if _usage is None:
                    errors.append(Error(
                        "Could not find item with id: ".format(usage_id),
                        "UsageModel.find_by_id({}) returned None".format(usage_id),
                        404,
                        "https://en.wikipedia.org/wiki/HTTP_404"))
                else:
                    scheduled_usage_value = scheduled_usage['value']
                    if scheduled_usage_value < _usage.min_value or scheduled_usage_value > _usage.max_value:
                        errors.append(Error(
                            "Given value is not in range of Usage values. ({} - {}) ({} given}".format(
                                _usage.min_value, _usage.max_value, scheduled_usage_value),
                            "value is not within range. ({} - {}) ({} given}".format(
                                _usage.min_value, _usage.max_value, scheduled_usage_value),
                            422,
                            "https://en.wikipedia.org/wiki/HTTP_404"
                        ))
                    if scheduled_usage['usage_id'] in seen_values:
                        errors.append(Error(
                            "Duplicate usage entry. {}".format(scheduled_usage['usage_id']),
                            "Duplicate usage entry. {}".format(scheduled_usage['usage_id']),
                            422,
                            "https://en.wikipedia.org/wiki/HTTP_422"
                        ))
                    seen_values.append(scheduled_usage['usage_id'])

    if "schedule_day_number" in kwargs:
        schedule_day_number = kwargs.pop("schedule_day_number")
        if schedule is None:
            pass
        else:
            for schedule_day in schedule.schedule_days:
                if schedule_day.day == schedule_day_number:
                    errors.append(Error(
                        "Given day ({}) is already being used by this schedule.".format(schedule_day_number),
                        "Given day ({}) is already being used by this schedule.".format(schedule_day_number),
                        422,
                        "https://en.wikipedia.org/wiki/HTTP_404"
                    ))
    if "schedule_day_id" in kwargs:
        schedule_day_id = kwargs.pop("schedule_day_id")
        schedule_day = ScheduleDayModel.find_by_id(schedule_day_id)
        if schedule_day is None:
            errors.append(Error(
                "Could not find schedule day with id: ".format(schedule_day_id),
                "ScheduleDayModel.find_by_id({}) returned None".format(schedule_day_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        if schedule is None:
            pass
        elif schedule.id != schedule_day.schedule_id:
            errors.append(Error(
                "The given schedule id did not match the days schedule id",
                "schedule.id != schedule_day.schedule_id",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))

    # SCHEDULED USAGE
    if "scheduled_usage_id" in kwargs:
        scheduled_usage_id = kwargs.pop("scheduled_usage_id")
        scheduled_usage = ScheduledUsageModel.find_by_id(scheduled_usage_id)
        if scheduled_usage is None:
            errors.append(Error(
                "Could not find scheduled usage with id: ".format(scheduled_usage_id),
                "ScheduledUsageModel.find_by_id({}) returned None".format(scheduled_usage_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        elif scheduled_usage.schedule_id != schedule.id:
            errors.append(Error(
                "The given schedule id did not match the scheduled usage schedule id",
                "scheduled_usage.schedule_id != schedule.id",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
    if "scheduled_usage_value" in kwargs:
        scheduled_usage_value = kwargs.pop("scheduled_usage_value")
        if scheduled_usage is not None:
            _usage = UsageModel.find_by_id(scheduled_usage.usage_id)
            if _usage.min_value > scheduled_usage_value or _usage.max_value < scheduled_usage_value:
                errors.append(Error(
                    "Given value is not in range of Usage values. ({} - {}) ({} given}".format(
                        _usage.min_value, _usage.max_value, scheduled_usage_value),
                    "value is not within range. ({} - {}) ({} given}".format(
                        _usage.min_value, _usage.max_value, scheduled_usage_value),
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_404"
                ))

    # METHOD SPECIFIC
    if method == "GroupItemResource.get":
        if item is None or group is None:
            pass
        elif not item.is_in_this_group(group.id):
            errors.append(Error(
                "Item with id {} is not in group with id {}".format(item.id, group.id),
                "item.is_in_this_group({}) returned False".format(group.id),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
    elif method == "GroupItemsResource.post":
        if item is None or group is None:
            pass
        elif item.is_in_this_group(group.id):
            errors.append(Error(
                "Item with id {} is already in group with id {}".format(item.id, group.id),
                "item is already in this group",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ))
        elif group.is_module is True:
            if item.is_in_module():
                errors.append(Error(
                    "Item cannot be in two different modules",
                    "item.is_in_module() returned True",
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_422"
                ))
    elif method == "GroupItemResource.delete":
        if item is None or group is None:
            pass
        elif not item.is_in_this_group(group.id):
            errors.append(Error("Item with id {} is not in group with id {}".format(item.id, group.id),
                                "item.is_in_this_group({}) returned False".format(group.id),
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
    elif method == "PresetActionsResource.post":
        if (group is not None) and (usage is not None):
            usage_is_in_group = False
            for item in group.items:
                if item.id == usage.item_id:
                    usage_is_in_group = True
            if not usage_is_in_group:
                errors.append(Error(
                    "The item that usage with id {} is attached to does not belong to group with id {}."
                        .format(usage.id, group.id),
                    "Usage is not in this group",
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_422"
                ))
    elif method == "ScheduledUsagesResource.post":
        if schedule is None or usage is None:
            pass
        else:
            for scheduled_usage in schedule.scheduled_usages:
                if scheduled_usage.usage_id == usage.id:
                    errors.append(Error(
                        "Given usage id is already being used by this schedule",
                        "usage id already in schedule",
                        422,
                        "https://en.wikipedia.org/wiki/HTTP_422"
                    ))

    assert len(kwargs) == 0, kwargs
    return errors
