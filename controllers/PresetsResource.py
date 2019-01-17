from flask_restful import Resource, request
from models.Preset import PresetModel
from models.Usage import UsageModel
from controllers.Validator import validate
from flask import current_app as app
import json
import requests


class PresetsResource(Resource):

    def get(self, group_id):
        all_presets = PresetModel.find_all_by_group_id(group_id) or []
        all_in_json = [preset.to_json() for preset in all_presets]
        return {"presets": all_in_json}, 200

    def post(self, group_id):
        if 'name' in request.form.keys():
            name = request.form['name']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']

        errors = validate(group_id=group_id, preset_name=name)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        preset = PresetModel(group_id, name)
        preset.save_to_db()
        return preset.to_json(), 201


class PresetResource(Resource):

    def get(self, group_id, preset_id):
        errors = validate(group_id=group_id, preset_id=preset_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        preset = PresetModel.find_by_id(preset_id)
        return preset.to_json()

    def put(self, group_id, preset_id):
        if 'name' in request.form.keys():
            name = request.form['name']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']

        errors = validate(group_id=group_id, preset_id=preset_id, preset_name=name)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        preset = PresetModel.find_by_id(preset_id)
        result = preset.set_name(name)
        if type(result) is PresetModel:
            return result.to_json(), 200
        else:
            return result, 400

    # @todo should this be patch?
    def patch(self, group_id, preset_id):
        errors = validate(group_id=group_id, preset_id=preset_id)
        if len(errors) > 0:
            return {"errors": [error.to_json for error in errors]}, 404

        preset = PresetModel.find_by_id(preset_id)
        responses = []
        for preset_action in preset.preset_actions:
            usage = UsageModel.find_by_id(preset_action.usage_id)
            response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'],
                                                                     usage.address, preset_action.value))
            responses.append(response)
        print(responses)
        return "Request has been accepted.", 202

    def delete(self, group_id, preset_id):
        errors = validate(group_id=group_id, preset_id=preset_id)
        if len(errors) > 0:
            return {"errors": [error.to_json for error in errors]}, 404

        preset = PresetModel.find_by_id(preset_id)
        preset.delete_from_db()
        return "Preset with id: {} was successfully deleted.".format(preset_id), 200
