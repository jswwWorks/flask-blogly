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
    """User Class."""

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
        db.Text,
        nullable=False
    )

class Post(db.Model):
    """Post class."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False,
        default="Working Title"
    )

    # Debating whether to make it db.Text or db.String(large num)
    content = db.Column(
        db.String(10000), # Typically it'll be db.Text -- db.Text has a built-in uppper bound ~64K
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False
    )

    user_id = db.Column(
        db.Integer, # good to make it explicit
        db.ForeignKey("users.id"), # Still give this a type (make it explicit)
        nullable=False
    )

