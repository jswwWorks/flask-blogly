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

    return render_template()


@