from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Usage import UsageModel
from models.Item import ItemModel
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum
from models.Error import Error
import json


class UsagesResource(Resource):

    def get(self):
        all_usages = UsageModel.find_all() or []
        all_in_json = [usage.to_json() for usage in all_usages]
        return {"usages": all_in_json}, 200

    def post(self):
        errors = []
        min_value = None
        max_value = None
        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
            external_item_id = request.form['external_item_id']
            consumption_type = request.form['consumption_type']
            consumption_amount = int(request.form['consumption_amount'])
            address = request.form['address']
            unit = request.form['unit']
            if 'min_value' in request.form.keys():
                min_value = request.form['min_value']
            if 'max_value' in request.form.keys():
                max_value = request.form['max_value']
        else:
            request_data = json.loads(request.data)

            item_id = request_data['item_id']
            external_item_id = request_data['external_item_id']
            consumption_type = request_data['consumption_type']
            consumption_amount = int(request_data['consumption_amount'])
            address = request_data['address']
            unit = request_data['unit']
            if 'min_value' in request_data.keys():
                min_value = request_data['min_value']
            if 'max_value' in request_data.keys():
                max_value = request_data['max_value']

        if UsageTypeEnum.has_value(consumption_type):
            consumption_type = UsageTypeEnum(consumption_type)
        else:
            errors.append(Error(
                "{} is not a valid consumption type.".format(consumption_type),
                "UsageTypeEnum.has_value({}) returned False".format(consumption_type),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))

        if UnitEnum.has_value(unit):
            unit = UnitEnum(unit)
        else:
            errors.append(Error(
                "{} is not a valid unit option.".format(unit),
                "UnitEnum.has_value({}) returned False".format(unit),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if ItemModel.find_by_id(item_id) is None:
            errors.append(Error(
                "Could not find item with id: ".format(item_id),
                "ItemMode.find_by_id({}) returned None".format(item_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        if len(address) < 3:
            errors.append(Error(
                "Address must be at least 4 characters long.",
                "address was {} characters long".format(len(address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if len(address) > 255:
            errors.append(Error(
                "Address cannot be longer than 255 characters.",
                "address was {} characters long".format(len(address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if consumption_amount < 0:
            errors.append(Error(
                "Consumption amount cannot be below 0.",
                "{} is below 0".format(consumption_amount),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if (min_value is None and max_value is not None) or (min_value is not None and max_value is None):
            errors.append(Error(
                "If either min or max value is given, both should be given.",
                "{} is below 0".format(consumption_amount),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if len(errors) > 0:
            return {errors: [error.to_json() for error in errors]}, 422
        usage = UsageModel(item_id, external_item_id, consumption_type, consumption_amount, address, unit, min_value, max_value)
        usage.save_to_db()
        return usage.to_json(), 201


class UsageResource(Resource):

    def get(self, usage_id):
        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            return 'Could not find Usage with id: {}'.format(usage_id), 404
        return usage.to_json()

    def put(self, usage_id):
        errors = []
        usage = UsageModel.find_by_id(usage_id)
        min_value = None
        max_value = None
        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
            external_item_id = request.form['external_item_id']
            consumption_type = request.form['consumption_type']
            consumption_amount = int(request.form['consumption_amount'])
            address = request.form['address']
            unit = request.form['unit']
            if 'min_value' in request.form.keys():
                min_value = request.form['min_value']
            if 'max_value' in request.form.keys():
                max_value = request.form['max_value']
        else:
            request_data = json.loads(request.data)

            item_id = request_data['item_id']
            external_item_id = request_data['external_item_id']
            consumption_type = request_data['consumption_type']
            consumption_amount = int(request_data['consumption_amount'])
            address = request_data['address']
            unit = request_data['unit']
            if 'min_value' in request_data.keys():
                min_value = request_data['min_value']
            if 'max_value' in request_data.keys():
                max_value = request_data['max_value']

        if UsageTypeEnum.has_value(consumption_type):
            consumption_type = UsageTypeEnum(consumption_type)
        else:
            errors.append(Error(
                "{} is not a valid consumption type.".format(consumption_type),
                "UsageTypeEnum.has_value({}) returned False".format(consumption_type),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))

        if UnitEnum.has_value(unit):
            unit = UnitEnum(unit)
        else:
            errors.append(Error(
                "{} is not a valid unit option.".format(unit),
                "UnitEnum.has_value({}) returned False".format(unit),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if ItemModel.find_by_id(item_id) is None:
            errors.append(Error(
                "Could not find item with id: ".format(item_id),
                "ItemMode.find_by_id({}) returned None".format(item_id),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404"))
        if len(address) < 3:
            errors.append(Error(
                "Address must be at least 4 characters long.",
                "address was {} characters long".format(len(address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if len(address) > 255:
            errors.append(Error(
                "Address cannot be longer than 255 characters.",
                "address was {} characters long".format(len(address)),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if consumption_amount < 0:
            errors.append(Error(
                "Consumption amount cannot be below 0.",
                "{} is below 0".format(consumption_amount),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if (min_value is None and max_value is not None) or (min_value is not None and max_value is None):
            errors.append(Error(
                "If either min or max value is given, both should be given.",
                "{} is below 0".format(consumption_amount),
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"))
        if len(errors) > 0:
            return {errors: [error.to_json() for error in errors]}, 422

        usage = usage.update(external_item_id=external_item_id,
                             consumption_type=consumption_type,
                             consumption_amount=consumption_amount,
                             address=address,
                             unit=unit,
                             min_value=min_value,
                             max_value=max_value)
        return usage.to_json(), 202


class CommandResource(Resource):

    def get(self, item_id, new_value):
        if new_value == 'tea':
            return "I'm a teapot", 418
        return 404, 404

    def post(self, usage_id, new_value):
        usage = UsageModel.find_by_id(usage_id)
        new_value = int(new_value)
        if usage.min_value > new_value or usage.max_value < new_value:
            return "New value does not fall within the expected range. ({} - {})".format(usage.min_value, usage.max_value), 400
        response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'], usage.address, new_value))
        return response.json()
