from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


class Monitors(Base):
    __tablename__ = 'active_monitors'

    dir_name = db.Column(db.String, nullable=False)

    def __init__(self, dir_name):
        self.dir_name = dir_name
