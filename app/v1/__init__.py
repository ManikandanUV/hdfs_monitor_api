from flask import Blueprint
from flask_restplus import Resource, Api, fields
from app import models

v1 = Blueprint('v1', __name__, url_prefix='/hdfs_monitor/v1')
api = Api(v1, version='1.0', title='Add/Remove HDFS directory monitors')

add_monitor_format = api.model('Add Monitor', {
    "path": fields.String(description="Monitored directory path", required=True)
})

rem_monitor_format = api.model('Remove Monitor', {
    "id": fields.Integer(description="Monitored directory id", required=True)
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
                           "path": new_monitor.dir_path}}, 200


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
