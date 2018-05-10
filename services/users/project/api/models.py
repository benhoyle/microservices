"""Model for User data."""
# services/users/project/api/model.py

from project import db


# model
class User(db.Model):
    """Model for a user."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        """Initialize object."""
        self.username = username
        self.email = email

    def to_json(self):
        """Return object as json."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }
