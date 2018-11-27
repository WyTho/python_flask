from flask import Flask
from flask_restful import Api
from controllers.ItemsResource import ItemsResource, ItemResource, CommandResource
from controllers.EventsResource import EventsResource, EventResource
from controllers.GroupsResource import GroupsResource, GroupResource
from controllers.EventCallResource import EventCallsResource, EventCallResource
from controllers.GraphResource import GraphsResource, GraphResource
from tests import clear_database, seed_test_data


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dev:secret@127.0.0.1:3306/test_env'
app.config['HOMELYNK_URI'] = 'http://remote:Selficient@10.1.1.10/scada-remote/request.cgi?m=json&r=grp&fn=write&'
api = Api(app)


api.add_resource(ItemsResource, '/api/item')
api.add_resource(ItemResource, '/api/item/<int:item_id>')
api.add_resource(CommandResource, '/api/item/<int:item_id>/command/<string:new_value>')

api.add_resource(EventsResource, '/api/event')
api.add_resource(EventResource, '/api/event/<int:event_id>')

api.add_resource(GroupsResource, '/api/group')
api.add_resource(GroupResource, '/api/group/<int:group_id>')

api.add_resource(EventCallsResource, '/api/event_call')
api.add_resource(EventCallResource, '/api/event_call/<int:event_call_id>')

api.add_resource(GraphsResource, '/api/graph')
api.add_resource(GraphResource, '/api/graph/<string:title>')

clear_database.clear_database()
# seed_test_data.seed_test_data()


if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(debug=True)

