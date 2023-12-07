"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



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
    new_user = User(first_name, last_name, image_url)

    return redirect("/users")

@app.get("/users<int:user_id>")
def show_user(user_id):
    """Routes get requests for each user page and maps corresponding response
    of rendering the user page.
    """

    user = User.query.filter_by(id = f"{user_id}").one()

    return render_template("user.html", user=user)

