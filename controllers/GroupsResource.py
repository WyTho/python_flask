from flask_restful import Resource, request
from models.Group import GroupModel
from models.ItemGroup import ItemGroupModel
from models.Item import ItemModel
from models.Error import Error
import json


class GroupsResource(Resource):

    def get(self):
        all_grousp = GroupModel.find_all() or []
        all_in_json = [group.to_json() for group in all_grousp]
        return {"groups": all_in_json}, 200

    def post(self):
        if 'name' in request.form.keys():
            name = request.form['name']
            is_module = request.form['is_module']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            is_module = request_data['is_module']
        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 255:
            return 'Name cannot be longer than 255 characters.', 400
        group = GroupModel(name, is_module)
        group.save_to_db()
        return group.to_json(), 201


class GroupResource(Resource):

    def get(self, group_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return "Cannot find group with id: {}".format(group_id), 404

        group = GroupModel.find_by_id(group_id)
        if group is None:
            return None
        return group.to_json()


    # @todo change this to ChangeName
    def put(self, group_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return "Cannot find group with id: {}".format(group_id), 404

        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
        else:
            request_data = json.loads(request.data)
            item_id = request_data['item_id']
        item = ItemModel.find_by_id(item_id)

        if item.is_in_this_group(group.id):
            item_group = ItemGroupModel.find_by_group_id_and_item_id(group.id, item.id)
            item_group.delete_from_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()

        if group.is_module is True:
            if not item.is_in_module():
                item_group = ItemGroupModel(item_id, group_id)
                item_group.save_to_db()
                group = GroupModel.find_by_id(group_id)
                return group.to_json()
            else:
                return 'Item cannot be in two different modules', 400
        else:
            item_group = ItemGroupModel(item_id, group_id)
            item_group.save_to_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()

    def delete(self, group_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return "Cannot find group with id: {}".format(group_id), 404

        group = GroupModel.find_by_id(group_id)
        group.delete_from_db()
        return "Group with id: {} was successfully deleted.".format(group_id), 200


class GroupItemsResource(Resource):
    def get(self, group_id):
        errors = []
        group = GroupModel.find_by_id(group_id)
        if group is None:
            errors.append(Error("Cannot find group with id: {}".format(group_id),
                                "GroupModel.find_by_id({}) returns None".format(group_id),
                                404,
                                "https://en.wikipedia.org/wiki/HTTP_404"))
        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 500

        items_from_group = ItemGroupModel.find_by_group_id(group_id)or []
        all_in_json = [item.to_json() for item in items_from_group]
        return {"items": all_in_json}, 200

    def post(self, group_id):
        errors = []
        group = GroupModel.find_by_id(group_id)
        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
        else:
            request_data = json.loads(request.data)
            item_id = request_data['item_id']
        item = ItemModel.find_by_id(item_id)

        if group is None:
            errors.append(Error("Cannot find group with id: {}".format(group_id),
                                "GroupModel.find_by_id({}) returns None".format(group_id),
                                404,
                                "https://en.wikipedia.org/wiki/HTTP_404"))
        if item is None:
            errors.append(Error("Cannot find item with id: {}".format(item_id),
                                "ItemModel.find_by_id({}) returns None".format(item_id),
                                404,
                                "https://en.wikipedia.org/wiki/HTTP_404"))

        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 500

        if item.is_in_this_group(group.id):
            errors.append(Error("Item with id {} is already in group with id {}".format(item_id, group_id),
                                "item is already in this group",
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))

        if group.is_module is True:
            if not item.is_in_module():
                item_group = ItemGroupModel(item_id, group_id)
                item_group.save_to_db()
                group = GroupModel.find_by_id(group_id)
                return group.to_json()
            else:
                return 'Item cannot be in two different modules', 400
        else:
            item_group = ItemGroupModel(item_id, group_id)
            item_group.save_to_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()


class GroupItemResource(Resource):
    def get(self, group_id, item_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return "Cannot find group with id: {}".format(group_id), 404

    def delete(self, group_id, item_id):
        group = GroupModel.find_by_id(group_id)
        if group is None:
            return "Cannot find group with id: {}".format(group_id), 404

