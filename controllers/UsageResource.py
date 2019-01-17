from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Usage import UsageModel
from models.Error import Error
from controllers.Validator import validate
import json
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


<<<<<<< HEAD
class CommandResource(Resource):
=======
    def get(self, usage_id, new_value):

        def hello():
            print("hello, world")
            h = httplib2.Http()
            h.follow_all_redirects = True
            resp, content = h.request("http://localhost:5000/api/items", "GET")

        t = threading.Timer(2.0, hello)
        t.start()  # after 30 seconds, "hello, world" will be printed

        if new_value == 'tea':
            return "I'm a teapot", 418
        return 404, 404
>>>>>>> development

    # @todo should this be patch?
    def patch(self, usage_id, new_value):
        usage = UsageModel.find_by_id(usage_id)
        new_value = int(new_value)
        if usage.min_value > new_value or usage.max_value < new_value:
            return {"errors": Error(
                "New value does not fall within the expected range. ({} - {})".format(usage.min_value, usage.max_value),
                "{} is outside of ({} - {})".format(new_value, usage.min_value, usage.max_value),
                422,
                ""
            ).to_json()}, 422
        response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'], usage.address, new_value))
        return response.json()
