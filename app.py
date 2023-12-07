"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

# FIXME: check on docstrings

@app.get("/")
def home_page():
    """Redirects to users list."""

    return redirect("/users")


@app.get("/users")
def show_users():
    """Takes nothing, shows tables using SQLAlchemy.
    Skeleton for application."""

    users = User.query.all()
    return render_template("list.html", users=users)

    # try:
    #     users = User.query.all()
    #     return render_template("list.html", users=users)
    # except:
    #     return render_template("list.html")


@app.get("/users/new")
def show_add_user_form():
    """Shows new user form."""

    return render_template('add-user.html')


@app.post("/users/new")
def create_new_user():
    """Adds form inputs to database and redirects to users page"""

    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]

    # TODO: What happens if forms are submitted with info the DB doesn't like?
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    # new_user = User()
    # db.session.add(new_user)
    # db.session.commit()

    # new_user.first_name = first_name
    # new_user.last_name = last_name
    # new_user.image_url = image_url
    # db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Routes get requests for each user page and maps corresponding response
    of rendering the user page.
    """

    user = User.query.filter_by(id = f"{user_id}").one()

    return render_template("user.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user_page(user_id):
    """Takes user_id, renders edit page for user."""

    user = User.query.filter_by(id = f"{user_id}").one()

    return render_template("edit-user.html", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit(user_id):
    """Takes user_id, renders edit page for user."""
    print("process_edit route", user_id)
    # Grab form inputs
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    status=request.form["action"]
    if status == "Cancel":
        return redirect("/users")
    # Process edits
    else:
        user = User.query.filter_by(id = f"{user_id}").one()

        # Override w/ changes (or leave defaults as need)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        # TODO: test to make sure edit feature works

        db.session.commit()

        return redirect ("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes user from database, redirects to /users homepage.
    """

    user = User.query.filter_by(id = f"{user_id}").one()
    db.session.delete(user)
    db.session.commit()

    return redirect ("/users")


