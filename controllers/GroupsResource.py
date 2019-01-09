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
        errors = []
        if 'name' in request.form.keys():
            name = request.form['name']
            is_module = request.form['is_module']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            is_module = request_data['is_module']
        if len(name) < 3:
            errors.append(Error("Name must be at least 3 characters long.",
                                "Name parameter must be at least 3 characters long.",
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
        elif len(name) > 255:
            errors.append(Error("Name cannot be longer than 255 characters.",
                                "Name parameter cannot be longer than 255 characters.",
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 400

        group = GroupModel(name, is_module)
        group.save_to_db()
        return group.to_json(), 201


class GroupResource(Resource):

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
        else:
            return group.to_json()

    def put(self, group_id):
        errors = []
        if 'name' in request.form.keys():
            name = request.form['name']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']

        group = GroupModel.find_by_id(group_id)

        if group is None:
            errors.append(Error("Cannot find group with id: {}".format(group_id),
                                "GroupModel.find_by_id({}) returned None".format(group_id),
                                404,
                                "https://en.wikipedia.org/wiki/HTTP_404"))
        if len(name) < 3:
            errors.append(Error("Name must be at least 3 characters long.",
                                "Name parameter must be at least 3 characters long.",
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
        elif len(name) > 255:
            errors.append(Error("Name cannot be longer than 255 characters.",
                                "Name parameter cannot be longer than 255 characters.",
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))

        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 500

        group = group.update_name(name)
        return group.to_json()

    def delete(self, group_id):
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
        else:
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

        item_groups_from_group = ItemGroupModel.find_by_group_id(group_id)or []
        all_in_json = [ItemModel.find_by_id(item_group.item_id).to_json() for item_group in item_groups_from_group]
        return {"items": all_in_json}, 200

    def post(self, group_id):
        errors = []
        if 'item_id' in request.form.keys():
            item_id = request.form['item_id']
        else:
            request_data = json.loads(request.data)
            item_id = request_data['item_id']
        group = GroupModel.find_by_id(group_id)
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
            return {'errors': all_errors_in_json}, 404

        if item.is_in_this_group(group.id):
            error = Error(
                "Item with id {} is already in group with id {}".format(item_id, group_id),
                "item is already in this group",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422")
            return {'errors': [error.to_json()]}, 404

        if group.is_module is True:
            if not item.is_in_module():
                item_group = ItemGroupModel(item_id, group_id)
                item_group.save_to_db()
                group = GroupModel.find_by_id(group_id)
                return group.to_json()
            else:
                error = Error(
                    "Item cannot be in two different modules",
                    "item.is_in_module() returned True",
                    422,
                    "https://en.wikipedia.org/wiki/HTTP_422"
                )
                return {'errors': [error.to_json()]}, 422
        else:
            item_group = ItemGroupModel(item_id, group_id)
            item_group.save_to_db()
            group = GroupModel.find_by_id(group_id)
            return group.to_json()


class GroupItemResource(Resource):
    def get(self, group_id, item_id):
        errors = []
        group = GroupModel.find_by_id(group_id)
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

        elif not item.is_in_this_group(group_id):
            errors.append(Error("Item with id {} is not in group with id {}".format(item_id, group_id),
                                "item.is_in_this_group({}) returned False".format(group_id),
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 500

        return item.to_json(), 200

    def delete(self, group_id, item_id):
        errors = []
        group = GroupModel.find_by_id(group_id)
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

        elif not item.is_in_this_group(group_id):
            errors.append(Error("Item with id {} is not in group with id {}".format(item_id, group_id),
                                "item.is_in_this_group({}) returned False".format(group_id),
                                400,
                                "https://en.wikipedia.org/wiki/HTTP_400"))
        if len(errors) > 0:
            all_errors_in_json = [error.to_json() for error in errors]
            return {'errors': all_errors_in_json}, 500

        item_group = ItemGroupModel.find_by_item_id_and_group_id(item_id, group_id)
        item_group.delete_from_db()
        item_group = ItemGroupModel.find_by_item_id_and_group_id(item_id, group_id)
        if item_group is not None:
            errors.append(Error("An unexpected error occurred item was not removed from group.",
                                "ItemGroupModel.find_by_item_id_and_group_id({}, {}) did not return None".format(item_id, group_id),
                                500,
                                "https://en.wikipedia.org/wiki/HTTP_500"))
        else:
            group = GroupModel.find_by_id(group_id)
            return group.to_json(), 200

