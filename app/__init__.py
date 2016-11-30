from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)