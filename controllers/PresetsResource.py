from flask_restful import Resource, request
from models.Preset import PresetModel
from models.Usage import UsageModel
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
        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 30:
            return 'Name cannot be longer than 30 characters.', 400
        preset = PresetModel(group_id, name)
        preset.save_to_db()
        return preset.to_json(), 201


class PresetResource(Resource):

    def get(self, group_id, preset_id):
        preset = PresetModel.find_by_id(preset_id)
        if preset is None:
            return "Could not find preset with id {}.".format(preset_id), 404
        return preset.to_json()

    def post(self, group_id, preset_id):
        preset = PresetModel.find_by_id(preset_id)
        if preset is None:
            return "Cannot find preset with id: {}".format(preset_id), 404
        if preset.group_id != group_id:
            return "The group id of the preset with id: {} did not match the given group id. " \
                   "Perhaps you are looking for a different preset?".format(preset_id), 400

        if 'name' in request.form.keys():
            name = request.form['name']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']

        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 30:
            return 'Name cannot be longer than 30 characters.', 400
        result = preset.set_name(name)
        if type(result) is PresetModel:
            return result.to_json(), 200
        else:
            return result, 400

    def patch(self, group_id, preset_id):
        preset = PresetModel.find_by_id(preset_id)
        if preset is None:
            return "Cannot find preset with id: {}.".format(preset_id), 404
        if preset.group_id != group_id:
            return "The group id of the preset with id: {} did not match the given group id. " \
                   "Perhaps you are looking for a different preset?".format(preset_id), 400

        request_data = json.loads(request.data)
        if "name" in request_data:
            name = request_data['name']
            result = preset.set_name(name)
            if type(result) is PresetModel:
                return result.to_json(), 200
            else:
                return result, 400
        if "status" in request_data:
            responses = []
            for preset_action in preset.preset_actions:
                usage = UsageModel.find_by_id(preset_action.usage_id)
                response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'],
                                                                         usage.address, preset_action.value))
                responses.append(response)
            print(responses)
            return "Request has been accepted.", 202

    def delete(self, group_id, preset_id):
        preset = PresetModel.find_by_id(preset_id)
        if preset is None:
            return "Cannot find preset with id: {}".format(preset_id), 404
        if preset.group_id != group_id:
            return "The group id of the preset with id: {} did not match the given group id. " \
                   "Perhaps you are looking for a different preset?".format(preset_id), 400

        preset.delete_from_db()
        return "Preset with id: {} was successfully deleted.".format(preset_id), 200
