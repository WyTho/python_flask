from flask_restful import Resource, request
from models.Item import ItemModel


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

        item = item.update(name=name, address=address, comment=comment)
        return item.to_json()
