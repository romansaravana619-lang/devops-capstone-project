"""Database models for the Account service."""
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when account data is invalid."""


class PersistentBase:
    """Persistent helper methods."""

    @classmethod
    def init_db(cls, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def create(self):
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        return cls.query.get(by_id)


class Account(db.Model, PersistentBase):
    """Account entity."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise DataValidationError("Invalid Account: body of request contained bad or no data")
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
        except KeyError as exc:
            raise DataValidationError(f"Invalid Account: missing {exc.args[0]}") from exc
        self.phone_number = data.get("phone_number")
        self.date_joined = date.fromisoformat(data["date_joined"]) if data.get("date_joined") else date.today()
        return self


def init_db(app):
    """Initialize the database."""
    Account.init_db(app)
