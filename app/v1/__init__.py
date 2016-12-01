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
                           "path": new_monitor.dir_name}}, 200


@api.route('/rem_monitor')
class RemoveMonitor(Resource):
    @api.response(200, 'Monitor Removed')
    @api.expect(rem_monitor_format, validate=True)
    def post(self):
        rem_monitor = models.Monitors.query.filter_by(id=(int(api.payload['id']))).first()
        if rem_monitor is None:
            return {"error": "ID not found"}, 404
        models.db.session.delete(rem_monitor)
        models.db.session.commit()
        return {"message": str(rem_monitor.id) + " removed successfully!"}, 200
