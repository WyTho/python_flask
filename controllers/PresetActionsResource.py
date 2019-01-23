from flask_restful import Resource, request
from models.PresetAction import PresetActionModel
from controllers.Validator import validate
import json


class PresetActionsResource(Resource):

    def get(self, group_id, preset_id):
        errors = validate(group_id=group_id, preset_id=preset_id)
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 404
        all_presets_actions = PresetActionModel.find_preset_actions_by_preset_id(preset_id) or []
        all_in_json = [preset.to_json() for preset in all_presets_actions]
        return {"preset_actions": all_in_json}, 200

    def post(self, group_id, preset_id):
        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            value = request.form['value']
        else:
            request_data = json.loads(request.data)
            usage_id = request_data['usage_id']
            value = request_data['value']

        errors = validate(
            group_id=group_id,
            preset_id=preset_id,
            usage_id=usage_id,
            usage_value=value,
            method="PresetActionsResource.post"
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422
        preset_action = PresetActionModel(preset_id, usage_id, value)
        preset_action.save_to_db()
        return preset_action.to_json(), 201


class PresetActionResource(Resource):

    def get(self, group_id, preset_id, preset_action_id):
        errors = validate(
            group_id=group_id,
            preset_id=preset_id,
            preset_action_id=preset_action_id
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422
        preset_action = PresetActionModel.find_by_id(preset_action_id)
        return preset_action.to_json()

    def put(self, group_id, preset_id, preset_action_id):
        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            value = request.form['value']
        else:
            request_data = json.loads(request.data)
            usage_id = request_data['usage_id']
            value = request_data['value']

        errors = validate(
            group_id=group_id,
            preset_id=preset_id,
            preset_action_id=preset_action_id,
            usage_id=usage_id,
            usage_value=value
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        preset_action = PresetActionModel.find_by_id(preset_action_id)
        preset_action.update(usage_id, value)
        return preset_action.to_json(), 200

    def delete(self, group_id, preset_id, preset_action_id):
        errors = validate(
            group_id=group_id,
            preset_id=preset_id,
            preset_action_id=preset_action_id
        )
        if len(errors) > 0:
            return {"errors": [error.to_json() for error in errors]}, 422

        preset_action = PresetActionModel.find_by_id(preset_action_id)
        preset_action.delete_from_db()
        return "Preset action with id: {} was successfully deleted.".format(preset_action_id), 200
