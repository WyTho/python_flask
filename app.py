from flask import Flask
from flask_restful import Api
from controllers.ItemsResource import ItemsResource, ItemResource
from controllers.EventsResource import EventsResource, EventResource


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 'mysql://username:password@ip:port/databasename'
api = Api(app)


api.add_resource(ItemsResource, '/item')
api.add_resource(ItemResource, '/item/<int:item_id>')

api.add_resource(EventsResource, '/event')
api.add_resource(EventResource, '/event/<int:event_id>')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
