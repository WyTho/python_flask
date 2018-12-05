from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Usage import UsageModel
from models.Item import ItemModel
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum
import json


class UsagesResource(Resource):

    def get(self):
        all_usages = UsageModel.find_all() or []
        all_in_json = [usage.to_json() for usage in all_usages]
        return {"usages": all_in_json}, 200

    def post(self):
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
            return '{} is not a valid consumption type.'.format(consumption_type), 400
        if UnitEnum.has_value(unit):
            unit = UnitEnum(unit)
        else:
            return '{} is not a valid unit option.'.format(unit), 400
        if ItemModel.find_by_id(item_id) is None:
            return 'Could not find item with id: '.format(item_id), 404
        if len(address) < 3:
            return 'Address must be at least 3 characters long.', 400
        if len(address) > 255:
            return 'Address cannot be longer than 255 characters.', 400
        if consumption_amount < 0:
            return 'Consumption amount cannot be below 0.', 400
        if (min_value is None and max_value is not None) or (min_value is not None and max_value is None):
            return 'If either min or max value is given, both should be given.', 400

        usage = UsageModel(item_id, external_item_id, consumption_type, consumption_amount, address, unit, min_value, max_value)
        usage.save_to_db()
        return usage.to_json(), 201


class UsageResource(Resource):

    def get(self, usage_id):
        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            return 'Could not find Usage with id: {}'.format(usage_id), 404
        return usage.to_json()

    def post(self, usage_id):
        usage = UsageModel.find_by_id(usage_id)
        min_value = None
        max_value = None
        if 'consumption_type' in request.form.keys():
            external_item_id = request.form['external_item_id']
            consumption_type = request.form['consumption_type']
            consumption_amount = int(request.form['consumption_amount'])
            address = request.form['address']
            unit = UnitEnum(request.form['unit'])
            if 'min_value' in request.form.keys():
                min_value = request.form['min_value']
            if 'max_value' in request.form.keys():
                max_value = request.form['max_value']
        else:
            request_data = json.loads(request.data)
            print(request_data['external_item_id'])
            consumption_type = request_data['consumption_type']
            consumption_amount = int(request_data['consumption_amount'])
            address = request_data['address']
            unit = request_data['unit']
            external_item_id = int(request_data['external_item_id'])
            if 'min_value' in request_data.keys():
                min_value = request_data['min_value']
            if 'max_value' in request_data.keys():
                max_value = request_data['max_value']

        if UsageTypeEnum.has_value(consumption_type):
            consumption_type = UsageTypeEnum(consumption_type)
        else:
            return '{} is not a valid consumption type.'.format(consumption_type), 400
        if UnitEnum.has_value(unit):
            unit = UnitEnum(unit)
        else:
            return '{} is not a valid unit option.'.format(unit), 400
        if len(address) < 3:
            return 'Address must be at least 3 characters long.', 400
        if len(address) > 255:
            return 'Address cannot be longer than 255 characters.', 400
        if consumption_amount < 0:
            return 'Consumption amount cannot be below 0.', 400
        if (min_value is None and max_value is not None) or (min_value is not None and max_value is None):
            return 'If either min or max value is given, both should be given.', 400

        usage = usage.update(external_item_id=external_item_id,
                             consumption_type=consumption_type,
                             consumption_amount=consumption_amount,
                             address=address,
                             unit=unit,
                             min_value=min_value,
                             max_value=max_value)
        return usage.to_json()


class CommandResource(Resource):

    def get(self, item_id, new_value):
        if new_value == 'tea':
            return "I'm a teapot", 418
        return 404, 404

    def post(self, usage_id, new_value):
        usage = UsageModel.find_by_id(usage_id)
        response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'], usage.address, new_value))
        return response.json()
