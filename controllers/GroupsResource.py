from flask_restful import Resource, request
from models.Group import GroupModel
from models.ItemGroup import ItemGroupModel
from models.Item import ItemModel


class GroupsResource(Resource):

    def get(self):
        all = GroupModel.find_all() or []
        all_in_json = [group.to_json() for group in all]
        return {"groups": all_in_json}, 200

    def post(self):
        name = request.form['name']
        is_module = request.form['is_module']
        group = GroupModel(name, is_module)
        group.save_to_db()
        return group.to_json(), 201


class GroupResource(Resource):

    def get(self, group_id):
        group = GroupModel.find_by_id(group_id)
        return group.to_json()

    def put(self, group_id):
        item_id = request.form['item_id']
        item = ItemModel.find_by_id(item_id)
        if not item.is_in_module:
            item_group = ItemGroupModel(item_id, group_id)
            item_group.save_to_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()
        else:
            raise ValueError('Item cannot be in two different modules')
