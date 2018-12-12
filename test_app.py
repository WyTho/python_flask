from flask import Flask
from flask_restful import Api
from controllers.ItemsResource import ItemsResource, ItemResource
from controllers.UsageResource import UsagesResource, UsageResource, CommandResource
from controllers.EventsResource import EventsResource, EventResource
from controllers.GroupsResource import GroupsResource, GroupResource
from controllers.EventCallResource import EventCallsResource, EventCallResource
from controllers.GraphResource import GraphsResource, GraphResource
from controllers.ScheduleResource import ScheduleResource, SchedulesResource
from controllers.ScheduledUsageResource import ScheduledUsagesResource, ScheduledUsageResource
from controllers.ScheduleDaysResource import ScheduleDayResource, ScheduleDaysResource


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dev:secret@127.0.0.1:3306/test_env'
app.config['HOMELYNK_URI'] = 'http://remote:Selficient@10.1.1.10/scada-remote/request.cgi?m=json&r=grp&fn=write&'
api = Api(app)

api.add_resource(ItemsResource, '/api/items')
api.add_resource(ItemResource, '/api/items/<int:item_id>')

api.add_resource(UsagesResource, '/api/usages')
api.add_resource(UsageResource, '/api/usages/<int:usage_id>')
api.add_resource(CommandResource, '/api/usages/<int:usage_id>/command/<string:new_value>')

api.add_resource(EventsResource, '/api/events')
api.add_resource(EventResource, '/api/events/<int:event_id>')

api.add_resource(GroupsResource, '/api/groups')
api.add_resource(GroupResource, '/api/groups/<int:group_id>')

api.add_resource(EventCallsResource, '/api/event_calls')
api.add_resource(EventCallResource, '/api/event_calls/<int:event_call_id>')

api.add_resource(GraphsResource, '/api/graphs')
api.add_resource(GraphResource, '/api/graphs/<string:title>')

api.add_resource(SchedulesResource, '/api/schedules')
api.add_resource(ScheduleResource, '/api/schedules/<int:schedule_id>')
api.add_resource(ScheduledUsagesResource, '/api/schedules/<int:schedule_id>/scheduled_usages')
api.add_resource(ScheduledUsageResource, '/api/schedules/<int:schedule_id>/scheduled_usages/<int:scheduled_usage_id>')
api.add_resource(ScheduleDayResource, '/api/schedules/<int:schedule_id>/schedule_days/<int:schedule_day_id>')
api.add_resource(ScheduleDaysResource, '/api/schedules/<int:schedule_id>/schedule_days')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(debug=True)


