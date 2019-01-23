from flask_restful import Resource, request
from models.Item import ItemModel
from models.UsageTypeEnum import UsageTypeEnum
from models.UnitEnum import UnitEnum
from models.Usage import UsageModel
import json
from controllers.Validator import validate


class ItemsResource(Resource):

    def get(self):
        all_items = ItemModel.find_all() or []
        all_in_json = [item.to_json() for item in all_items]
        return {"items": all_in_json}, 200

    def post(self):
        if 'name' in request.form.keys():
            name = request.form['name']
            comment = request.form['comment']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            comment = request_data['comment']

        errors = validate(item_name=name, item_comment=comment)

        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422
        item = ItemModel(name, comment)
        item.save_to_db()
        return item.to_json(), 201


class ItemResource(Resource):

    def get(self, item_id):
        errors = validate(item_id=item_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        return ItemModel.find_by_id(item_id).to_json()

    # @todo should this be removed?
    def put(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if 'name' in request.form.keys():
            name = request.form['name']
            comment = request.form['comment']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            comment = request_data['comment']

        errors = validate(item_id=item_id, item_name=name, item_comment=comment)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        item = item.update(name=name, comment=comment)
        return item.to_json()


class ItemUsagesResource(Resource):

    def get(self, item_id):
        errors = validate(item_id=item_id)
        if len(errors) > 0:
            return {'errors': [error.to_json() for error in errors]}, 404

        item = ItemModel.find_by_id(item_id)
        usages_in_json = [usage.to_json() for usage in item.usages]
        return {"usages": usages_in_json}, 200

    def post(self, item_id):
        min_value = None
        max_value = None
        if 'external_item_id' in request.form.keys():
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
            item_id=item_id,
            usage_consumption_type=consumption_type,
            usage_consumption_amount=consumption_amount,
            usage_address=address,
            usage_unit=unit,
            usage_min_value=min_value,
            usage_max_value=max_value
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        consumption_type = UsageTypeEnum(consumption_type)
        unit = UnitEnum(unit)
        usage = UsageModel(item_id, external_item_id, consumption_type, consumption_amount, address, unit, min_value, max_value)
        usage.save_to_db()
        return usage.to_json(), 201


class ItemUsageResource(Resource):

    def get(self, item_id, usage_id):
        errors = validate(item_id=item_id, usage_id=usage_id)
        if len(errors) > 0:
            return {errors: [error.to_json() for error in errors]}, 404

        usage = UsageModel.find_by_id(usage_id)
        return {"usage": usage.to_json()}, 200

    def put(self, item_id, usage_id):
        min_value = None
        max_value = None
        if 'external_item_id' in request.form.keys():
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
            item_id=item_id,
            usage_id=usage_id,
            usage_consumption_amount=consumption_amount,
            usage_consumption_type=consumption_type,
            usage_address=address,
            usage_unit=unit,
            usage_min_value=min_value,
            usage_max_value=max_value
        )

        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404

        usage = UsageModel.find_by_id(usage_id)
        usage = usage.update(external_item_id=external_item_id,
                             consumption_type=consumption_type,
                             consumption_amount=consumption_amount,
                             address=address,
                             unit=unit,
                             min_value=min_value,
                             max_value=max_value)
        return usage.to_json(), 202

    def delete(self, item_id, usage_id):
        errors = validate(item_id=item_id, usage_id=usage_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422
        usage = UsageModel.find_by_id(usage_id)
        usage.delete_from_db()