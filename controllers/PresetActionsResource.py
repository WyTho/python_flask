from flask_restful import Resource, request
from models.PresetAction import PresetActionModel
from models.Usage import UsageModel
from models.Group import GroupModel
import json


class PresetActionsResource(Resource):

    def get(self, group_id, preset_id):
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
        group = GroupModel.find_by_id(group_id)
        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            return 'Could not find Usage with id: {}.'.format(usage_id), 404
        if value < usage.min_value or value > usage.max_value:
            return 'Given value is not in range of Usage values. ({} - {}) ({} given)' \
                       .format(usage.min_value, usage.max_value, value), 400
        if group is None:
            return "Could not find Group with id: {}.".format(group_id), 404
        usage_is_in_group = False
        for item in group.items:
            if item.id == usage.item_id:
                usage_is_in_group = True
        if not usage_is_in_group:
            return "The item that usage with id {} is attached to does not belong to group with id {}." \
                       .format(usage.id, group_id), 400
        preset_action = PresetActionModel(preset_id, usage_id, value)
        preset_action.save_to_db()
        return preset_action.to_json(), 201


class PresetActionResource(Resource):

    def get(self, group_id, preset_id, preset_action_id):
        preset_action = PresetActionModel.find_by_id(preset_action_id)
        if preset_action is None:
            return "Could not find preset action with id {}.".format(preset_action_id), 404
        return preset_action.to_json()

    def put(self, group_id, preset_id, preset_action_id):
        preset_action = PresetActionModel.find_by_id(preset_action_id)
        if preset_action is None:
            return "Could not find preset action with id: {}.".format(preset_action_id), 404
        if preset_action.preset_id != preset_id:
            return "The preset id of the preset action with id: {} did not match the given preset id. " \
                   "Perhaps you are looking for a different preset action?".format(preset_action_id), 400

        if 'usage_id' in request.form.keys():
            usage_id = request.form['usage_id']
            value = request.form['value']
        else:
            request_data = json.loads(request.data)
            usage_id = request_data['usage_id']
            value = request_data['value']
        usage = UsageModel.find_by_id(usage_id)
        if usage is None:
            return 'Could not find Usage with id: {}.'.format(usage_id), 404
        if value < usage.min_value or value > usage.max_value:
            return 'Given value is not in range of Usage values. ({} - {}) ({} given)'\
                .format(usage.min_value, usage.max_value, value), 400

        preset_action.update(usage_id, value)
        return preset_action.to_json(), 200

    def delete(self, group_id, preset_id, preset_action_id):
        preset_action = PresetActionModel.find_by_id(preset_action_id)
        if preset_action is None:
            return "Cannot find preset with id: {}".format(preset_id), 404
        if preset_action.preset_id != preset_id:
            return "The preset id of the preset action with id: {} did not match the given preset id. " \
                   "Perhaps you are looking for a different preset action?".format(preset_action_id), 400

        preset_action.delete_from_db()
        return "Preset action with id: {} was successfully deleted.".format(preset_action_id), 200
