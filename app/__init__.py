from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
db = SQLAlchemy(app)


from app.v1 import v1

app.register_blueprint(v1)

if __name__ == '__main__':
    app.run(debug=True)