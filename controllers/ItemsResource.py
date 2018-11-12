from flask_restful import Resource, request
import requests
from flask import current_app as app
from models.Item import ItemModel
from models.UsageTypeEnum import UsageTypeEnum


class ItemsResource(Resource):

    def get(self):
        all = ItemModel.find_all() or []
        all_in_json = [item.to_json() for item in all]
        return {"items": all_in_json}, 200

    def post(self):
        name = request.form['name']
        address = request.form['address']
        comment = request.form['comment']
        item = ItemModel(name, address, comment)
        item.save_to_db()
        return item.to_json(), 201


class ItemResource(Resource):

    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        return item.to_json()

    def post(self, item_id):
        item = ItemModel.find_by_id(item_id)

        name = request.form['name']
        address = request.form['address']
        comment = request.form['comment']
        usage_type = request.form['usage_type']
        usage = request.form['usage']

        item = item.update(name=name, address=address, comment=comment, usage_type=usage_type, usage=usage)
        return item.to_json()


class CommandResource(Resource):

    def post(self, item_id, new_value):
        item = ItemModel.find_by_id(item_id)
        url = "{}alias={}&value={}".format(app.config['HOMELYNK_URI'], item.address, new_value)
        print(url)
        response = requests.get(url="{}alias={}&value={}".format(app.config['HOMELYNK_URI'], item.address, new_value))
        print(response)
        return response.json()
