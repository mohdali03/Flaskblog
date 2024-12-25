
from flask import render_template, flash, redirect, url_for
from datetime import datetime
from sqlalchemy import or_
from flaskblog.forms import SignUpForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post, db
from flask import current_app as app

posts = [
    {
        "id": 1,
        "title": "How to Learn Python",
        "author": "Alice",
        "content": "Python is a versatile programming language. Start with basics like variables, loops, and functions.",
        "date_posted": "2024-12-21",
        "comments": [
            {
                "author": "Bob",
                "content": "Great post! Very helpful for beginners.",
                "date_posted": "2024-12-22"
            },
            {
                "author": "Charlie",
                "content": "Thanks for sharing these tips.",
                "date_posted": "2024-12-23"
            }
        ]
    },
    {
        "id": 2,
        "title": "Flask vs Django: Which Framework to Choose",
        "author": "David",
        "content": "Choosing between Flask and Django depends on your project needs. Flask is lightweight, while Django is feature-rich.",
        "date_posted": "2024-12-20",
        "comments": [
            {
                "author": "Eve",
                "content": "I prefer Flask for small projects.",
                "date_posted": "2024-12-21"
            },
            {
                "author": "Frank",
                "content": "Django's admin panel is amazing for large apps!",
                "date_posted": "2024-12-21"
            }
        ]
    },
    {
        "id": 3,
        "title": "Getting Started with SQL",
        "author": "Grace",
        "content": "SQL is essential for managing databases. Learn how to write SELECT, INSERT, UPDATE, and DELETE queries.",
        "date_posted": "2024-12-19",
        "comments": []
    }
]

@app.route("/")
def home():
    return render_template('index.html', posts=posts, title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            or_(User.email == form.email.data, User.username == form.username.data)  # type: ignore
        ).first()
        
        if existing_user:
            if existing_user.email == form.email.data:
                flash("Email already in use. Please choose a different one.", "danger")
            elif existing_user.username == form.username.data:
                flash("Username already in use. Please choose a different one.", "danger")
            return redirect(url_for('register'))
        
        hashPassword = generate_password_hash(form.password.data) # type: ignore
        username = form.username.data
        email = form.email.data
        newUser = User(        
            username,
            email,
            hashPassword)
        print(newUser)
        db.session.add(newUser)
        db.session.commit()
        
        flash(f"Acccount Created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user:
            
            
        if user and check_password_hash(user.password, form.password.data): # type: ignore
            flash(f"login Success! Welcome, {user.username}!", "success" )
            return redirect(url_for('home'))
        elif not user:
            flash(f"You don't Have Account! Register first", 'danger')
        # if form.email.data =="ali@gmail.com" and form.password.data =="ali123":
        #     username = form.email.data.split("@")
        #     flash(f"Login Succes {username[0]}!", "success")
        else:
            flash(f"Login UnsuccessFull. Please check email & password", 'danger')
    return render_template('login.html', title='Login', form=form)