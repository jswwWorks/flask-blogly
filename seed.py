"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# Pet.query.delete()

# Add pets
# nick = User(first_name='Nick', last_name="Orsi")
# julia = User(first_name='Julia', last_name="Williamson")


# # Add new objects to session, so they'll persist
# db.session.add(nick)
# db.session.add(julia)

# # Commit--otherwise, this never gets saved!
# db.session.commit()