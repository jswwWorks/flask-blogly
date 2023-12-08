"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

# Make instance of SQLAlchemy class to work with
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Class with properties serial id, first_name, last_name, and
    image_url."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # First and last name should be required
    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    # TODO: in further study, add a default image
    image_url = db.Column(
        db.String(1000),
        nullable=False
    )
