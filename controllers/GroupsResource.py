from flask_restful import Resource, request
from models.Group import GroupModel
from models.ItemGroup import ItemGroupModel
from models.Item import ItemModel
import json


class GroupsResource(Resource):

    def get(self):
        all = GroupModel.find_all() or []
        all_in_json = [group.to_json() for group in all]
        return {"groups": all_in_json}, 200

    def post(self):
        if 'name' in request.form.keys():
            name = request.form['name']
            is_module = request.form['is_module']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            is_module = request_data['is_module']
        group = GroupModel(name, is_module)
        group.save_to_db()
        return group.to_json(), 201


class GroupResource(Resource):

    def get(self, group_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return None
        return group.to_json()

    def put(self, group_id):
        # @ todo remove item from group if already in this group
        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
        else:
            request_data = json.loads(request.data)
            item_id = request_data['item_id']
        item = ItemModel.find_by_id(item_id)
        if not item.is_in_module():
            item_group = ItemGroupModel(item_id, group_id)
            item_group.save_to_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()
        else:
            return 'Item cannot be in two different modules', 400
