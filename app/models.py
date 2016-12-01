from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Monitors(Base):
    __tablename__ = 'active_monitors'

    dir_path = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def __init__(self, dir_path, is_active = True):
        """
        :string dir_path: Directory path to be monitored
        :boolean is_active: Is the directory active for monitoring
        """
        self.dir_path = dir_path
        self.is_active = is_active
