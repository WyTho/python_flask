from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Usage import UsageModel
from models.Item import ItemModel
from models.Error import Error
from controllers.Validator import validate
import json
from datetime import datetime
import threading
import httplib2


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

        errors = validate(
            usage_unit=unit,
            item_id=item_id,
            usage_address=address,
            usage_consumption_type=consumption_type,
            usage_consumption_amount=consumption_amount,
            usage_min_value=min_value,
            usage_max_value=max_value
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        usage = UsageModel(item_id, external_item_id, consumption_type, consumption_amount, address, unit, min_value, max_value)
        usage.save_to_db()
        return usage.to_json(), 201


class UsageResource(Resource):

    def get(self, usage_id):
        errors = validate(usage_id=usage_id)
        if len(errors) > 0:
            return {errors: [error.to_json() for error in errors]}, 404
        usage = UsageModel.find_by_id(usage_id)
        return usage.to_json()

    def put(self, usage_id):
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

        errors = validate(
            usage_id=usage_id,
            usage_unit=unit,
            item_id=item_id,
            usage_address=address,
            usage_consumption_amount=consumption_amount,
            usage_min_value=min_value,
            usage_max_value=max_value
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        usage = UsageModel.find_by_id(usage_id)
        usage = usage.update(
            external_item_id=external_item_id,
            consumption_type=consumption_type,
            consumption_amount=consumption_amount,
            address=address,
            unit=unit,
            min_value=min_value,
            max_value=max_value)
        return usage.to_json(), 200


class CommandResource(Resource):

    # @todo should this be patch?
    def patch(self, usage_id, new_value):
        usage = UsageModel.find_by_id(usage_id)
        new_value = float(new_value)
        if usage.min_value > new_value or usage.max_value < new_value:
            return {"errors": Error(
                "New value does not fall within the expected range. ({} - {})".format(usage.min_value, usage.max_value),
                "{} is outside of ({} - {})".format(new_value, usage.min_value, usage.max_value),
                422,
                ""
            ).to_json()}, 422
        print("url is: " + "{}/{}/{}".format(app.config['HOMELYNK_URI'], usage.external_item_id, new_value))
        response = requests.get(url="{}/{}/{}".format(app.config['HOMELYNK_URI'], usage.external_item_id, int(new_value)))
        home_response = response.json()
        item = ItemModel.find_by_id(usage.item_id)
        item_in_json = item.to_json()
        fake_event = {
                'last_use_timestamp': datetime.now().timestamp(),
                'data_type': usage.unit.value,
                'data': float(home_response["current_value"]),
                'usage_id': usage.id
            }
        item_in_json['last_use'] = fake_event
        return item_in_json, 200
