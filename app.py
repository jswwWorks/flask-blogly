"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from data import validate_names

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get("/")
def home_page():
    """Redirects to users /users."""

    return redirect("/users")


@app.get("/users")
def list_users():
    """Takes nothing, accesses data base for all current users and renders the
    list.html to list all first and last names of current users in database."""

    users = User.query.all()
    return render_template("list.html", users=users)



@app.get("/users/new")
def show_add_user_form():
    """Shows new user form."""

    return render_template('add-user.html')


@app.post("/users/new")
def create_new_user():
    """Takes nothing, grabs user inputs from form. Validates inputs. If invalid,
    returns user /users/new. If valid, adds form inputs to database and
    redirects to /users page."""

    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]

    # result will either be a list of first_name and last_name with any
    # whitespace stripped, or if inputs are empty, result will be False.
    result = validate_names(first_name, last_name)

    if result == False:
        # Send user back to new users form if they had invalid input(s)

        flash('Please try again.' +
            ' First and last names must each contain at least 1 character.')
        return redirect("/users/new")
    # If result not False create new user
    new_user = User(
        first_name=result[0],
        last_name=result[1],
        image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Routes get requests for each user page and renders the respective user
    page. Takes user_id from URL."""

    user = User.query.filter_by(id = f"{user_id}").one()

    return render_template("user.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user_page(user_id):
    """Takes user_id from URL, renders edit page for user."""

    user = User.query.filter_by(id = f"{user_id}").one()

    return render_template("edit-user.html", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit(user_id):
    """Takes user_id from URL, gathers inputs from the form, determines if
    user clicked on cancel.
    If so redirects to /users page without updating database.
    If user clicked save, gathers inputs from the form, validates data.
        If invalid, redirects to /users/<int:user_id>/edit and flashes message.
        If valid, updates the database, and redirects to /users page.
    """

    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    status=request.form["action"]

    if status == "Cancel":
        return redirect("/users")

    else:
        user = User.query.filter_by(id = f"{user_id}").one()

        # Validate inputs
        result = validate_names(first_name, last_name)

        if result == False:
            # Send user back to new users form if they had invalid input(s)
            flash('Please try again.' +
                ' First and last names must each contain at least 1 character.')
            return redirect(f"/users/{user_id}/edit")

        # If result not False override w/ changes (or leave defaults as need)
        user.first_name = result[0]
        user.last_name = result[1]
        user.image_url = image_url

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


