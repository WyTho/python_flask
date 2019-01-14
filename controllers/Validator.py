from models.Item import ItemModel
from models.Usage import UsageModel
from models.Error import Error
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum


def validate(**kwargs):
    errors = []
    item_id = None


    # ITEM
    if "item_id" in kwargs:
        item_id = kwargs.pop("item_id")
        if ItemModel.find_by_id(item_id) is None:
            errors.append(Error(
                "Could not find item with id: ".format(item_id),
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
        if UsageModel.find_by_id(usage_id) is None:
            errors.append(Error(
                "Could not find item with id: ".format(usage_id),
                "UsageModel.find_by_id({}) returned None".format(usage_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        if item_id is not None:
            if ItemModel.find_by_id(item_id).has_usage(usage_id):
                errors.append(Error(
                    "Could not find usage with id: ".format(usage_id),
                    "UsageModel.find_by_id({}) returned None".format(usage_id),
                    404,
                    "https://en.wikipedia.org/wiki/HTTP_404"))

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

    return errors
