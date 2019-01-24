from flask import Flask
from flask_restful import Api
from controllers.ItemsResource import ItemsResource, ItemResource, ItemUsageResource, ItemUsagesResource
from controllers.EventsResource import EventsResource, EventResource
from controllers.GroupsResource import GroupsResource, GroupResource, GroupItemResource, GroupItemsResource
from controllers.PresetsResource import PresetResource, PresetsResource
from controllers.PresetActionsResource import PresetActionResource, PresetActionsResource
from controllers.EventCallResource import EventCallsResource, EventCallResource
from controllers.GraphResource import GraphsResource, GraphResource
from controllers.UsageResource import UsageResource, UsagesResource, CommandResource
from controllers.ScheduleResource import ScheduleResource, SchedulesResource
from controllers.ScheduledUsageResource import ScheduledUsageResource, ScheduledUsagesResource
from controllers.ScheduleDaysResource import ScheduleDaysResource, ScheduleDayResource
from controllers.AnalyzeEventsResource import AnalyzeEventsResource

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dev:secret@127.0.0.1:3306/WySmart'  # 'mysql://username:password@ip:port/databasename'
app.config['HOMELYNK_URI'] = 'http://192.168.8.155:5000/api/objects'
app.config['API_URI'] = '127.0.0.1:5000/api/v1/'
api = Api(app)
baseurl = "/api/v1/"

api.add_resource(ItemsResource, baseurl+'items')
api.add_resource(ItemResource, baseurl+'items/<int:item_id>')
api.add_resource(ItemUsageResource, baseurl+'items/<int:item_id>/usages')
api.add_resource(ItemUsagesResource, baseurl+'items/<int:item_id>/usages/<int:usage_id>')

api.add_resource(UsagesResource, baseurl+'usages')
api.add_resource(UsageResource, baseurl+'usages/<int:usage_id>')
api.add_resource(CommandResource, baseurl+'usages/<int:usage_id>/command/<string:new_value>')

api.add_resource(EventsResource, baseurl+'events')
api.add_resource(EventResource, baseurl+'events/<int:event_id>')

api.add_resource(GroupsResource, baseurl+'groups')
api.add_resource(GroupResource, baseurl+'groups/<int:group_id>')
api.add_resource(GroupItemsResource, baseurl+'groups/<int:group_id>/items')
api.add_resource(GroupItemResource, baseurl+'groups/<int:group_id>/items/<int:item_id>')
api.add_resource(PresetsResource, baseurl+'groups/<int:group_id>/presets')
api.add_resource(PresetResource, baseurl+'groups/<int:group_id>/presets/<int:preset_id>')
api.add_resource(PresetActionsResource, baseurl+'groups/<int:group_id>/presets/<int:preset_id>/preset_actions')
api.add_resource(PresetActionResource, baseurl+'groups/<int:group_id>/presets/<int:preset_id>/preset_actions'
                                               '<int:preset_action_id>')

api.add_resource(EventCallsResource, baseurl+'event_calls')
api.add_resource(EventCallResource, baseurl+'event_calls/<int:event_call_id>')

api.add_resource(GraphsResource, baseurl+'graphs')
api.add_resource(GraphResource, baseurl+'graphs/<string:title>')

api.add_resource(SchedulesResource, baseurl+'schedules')
api.add_resource(ScheduleResource, baseurl+'schedules/<int:schedule_id>')
api.add_resource(ScheduledUsagesResource, baseurl+'schedules/<int:schedule_id>/scheduled_usages')
api.add_resource(ScheduledUsageResource, baseurl+'schedules/<int:schedule_id>/scheduled_usages/<int:scheduled_usage_id>')
api.add_resource(ScheduleDayResource, baseurl+'schedules/<int:schedule_id>/schedule_days/<int:schedule_day_id>')
api.add_resource(ScheduleDaysResource, baseurl+'schedules/<int:schedule_id>/schedule_days')

# For fake-data analysis
api.add_resource(AnalyzeEventsResource, baseurl+'events/analyze')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(debug=True, host='0.0.0.0')


