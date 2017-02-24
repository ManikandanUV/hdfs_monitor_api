import datetime

from flask import Blueprint
from flask_restplus import Resource, Api, fields, reqparse
from app import models

v1 = Blueprint('v1', __name__, url_prefix='/hdfs_monitor/v1')
api = Api(v1, version='1.0', title='Add/Remove HDFS directory monitors')

add_monitor_format = api.model('Add Monitor', {
    "path": fields.String(description="Monitored directory path", required=True)
})

rem_monitor_format = api.model('Remove Monitor', {
    "id": fields.Integer(description="Monitored directory id", required=True)
})

message_log_format = api.model('Log Message', {
    "timestamp": fields.DateTime(description="Event timestamp", required=True),
    "dir_id": fields.Integer(description="Monitored directory id", required=True),
    "filename": fields.String(description="File name only", required=True),
    "message": fields.String(description="Message published", required=True)
})


@api.route('/add_monitor')
class AddMonitor(Resource):
    @api.response(200, 'Monitor Added')
    @api.expect(add_monitor_format, validate=True)
    def post(self):
        print(api.payload)
        new_monitor = models.Monitors(api.payload['path'])
        models.db.session.add(new_monitor)
        models.db.session.commit()
        return {"message": "Monitor added successfully!",
                "record": {"id": new_monitor.id,
                           "path": new_monitor.dir_path}}, 201


@api.route('/rem_monitor')
class RemoveMonitor(Resource):
    @api.response(200, 'Monitor Removed')
    @api.expect(rem_monitor_format, validate=True)
    def post(self):
        rem_monitor = models.Monitors.query.filter_by(id=(int(api.payload['id']))).first()
        if rem_monitor is None:
            return {"error": "ID not found"}, 404
        rem_monitor.is_active = False
        models.db.session.commit()
        return {"message": str(rem_monitor.id) + " removed successfully!"}, 200


@api.route('/get_monitors')
class GetMonitors(Resource):
    def get(self):
        active_monitors = models.Monitors.query.filter_by(is_active=True).all()
        print(active_monitors)
        if active_monitors is None:
            return {"error": "no active monitors found"}, 404
        active_monitor_list = []
        for monitor in active_monitors:
            active_monitor_list.append({'id': monitor.id, 'dir_path': monitor.dir_path})
        return {"active_monitors": active_monitor_list}, 200


@api.route('/log_event')
class LogMessage(Resource):
    @api.response(200, 'Event Log Created')
    @api.expect(message_log_format, validate=True)
    def post(self):
        event_timestamp = datetime.datetime.strptime(api.payload['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        new_message = models.Messages(date_created=event_timestamp,
                                      dir_id=api.payload['dir_id'],
                                      filename=api.payload['filename'],
                                      message=api.payload['message'])
        models.db.session.add(new_message)
        models.db.session.commit()
        response = {"message": "event id #" + str(new_message.id) + " logged successfully"}
        code = 201
        return response, code


@api.route('/get_events')
class GetEvents(Resource):
    @api.doc(params={'dir_id': 'Monitor ID',
                     'max_events': 'Maximum number of events'})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dir_id', type=int, required=True)
        parser.add_argument('max_events', type=int)
        args = parser.parse_args()

        if int(args['dir_id']) < 0:
            response = {'error': 'invalid monitor id ' + args['dir_id']}
            code = 400
            return response, code

        if int(args['max_events']) < 1:
            response = {'error': 'invalid max_events size ' + args['max_events']}
            code = 400
            return response, code

        dir_events = models.Messages.query.filter_by(dir_id=args['dir_id']).limit(args['max_events']).all()
        return dir_events
