from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Item import ItemModel
import json

class ItemsResource(Resource):

    def get(self):
        all = ItemModel.find_all() or []
        all_in_json = [item.to_json() for item in all]
        return {"items": all_in_json}, 200

    def post(self):
        if 'name' in request.form.keys():
            name = request.form['name']
            address = request.form['address']
            comment = request.form['comment']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            address = request_data['address']
            comment = request_data['comment']
        # request_data = json.loads(request.data)
        # name = request.form['name']
        # address = request.form['address']
        # comment = request.form['comment']
        item = ItemModel(name, address, comment)
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
            address = request.form['address']
            comment = request.form['comment']
        else:
            request_data = json.loads(request.data)
            name = request_data['name']
            address = request_data['address']
            comment = request_data['comment']

        item = item.update(name=name, address=address, comment=comment)
        return item.to_json()


class CommandResource(Resource):

    def get(self, item_id, new_value):
        if new_value == 'tea':
            return "I'm a teapot", 418
        return 404, 404

    def post(self, item_id, new_value):
        item = ItemModel.find_by_id(item_id)
        response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'], item.address, new_value))
        return response.json()
