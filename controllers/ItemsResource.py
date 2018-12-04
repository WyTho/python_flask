from flask_restful import Resource, request
from models.Item import ItemModel
import json


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

        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 255:
            return 'Name cannot be longer than 255 characters.', 400
        if len(comment) > 255:
            return 'Comment cannot be longer than 255 characters.', 400

        item = ItemModel(name, comment)
        item.save_to_db()
        return item.to_json(), 201


class ItemResource(Resource):

    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if item is None:
            return None
        return item.to_json()

    def post(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if 'name' in request.form.keys():
            name = request.form['name']
            comment = request.form['comment']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            comment = request_data['comment']

        if len(name) < 3:
            return 'Name must be at least 3 characters long.', 400
        if len(name) > 255:
            return 'Name cannot be longer than 255 characters.', 400
        if len(comment) > 255:
            return 'Comment cannot be longer than 255 characters.', 400

        item = item.update(name=name, comment=comment)
        return item.to_json()
