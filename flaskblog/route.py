import os
import secrets
# from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
# from sqlalchemy import or_
from .forms import SignUpForm, LoginForm,UpdateAccountForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post, db
from flask import current_app as app
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
       
        hashpassword = generate_password_hash(form.password.data) # type: ignore    
        user = User(username=form.username.data, email=form.email.data, password=hashpassword)# type: ignore
        # print(user)
        db.session.add(user)
        db.session.commit()
        
        flash(f"Acccount Created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user:
            
            
        if user and check_password_hash(user.password, form.password.data): # type: ignore
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            flash(f"login Success! Welcome, {user.username}!", "success" )
            print(next_page)
            return redirect(next_page) if next_page and next_page.startswith('/') else redirect(url_for('home'))
        elif not user:
            flash(f"You don't Have Account! Register first", 'danger')
            return redirect(url_for('register'))
        # if form.email.data =="ali@gmail.com" and form.password.data =="ali123":
        #     username = form.email.data.split("@")
        #     flash(f"Login Succes {username[0]}!", "success")
        else:
            flash(f"Login UnsuccessFull. Please check email & password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")

    return redirect(url_for('home'))

def save_picture(form_picture):
    # Generate a random file name to avoid conflicts
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    output_size= (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save the uploaded file
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
            print(f"Uploaded Picture: {picture_file}")
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Pre-fill the form with current user's data
        form.username.data = current_user.username
        form.email.data = current_user.email

    if current_user.img_file:
        img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    else:
        img_file = url_for('static', filename='profile_pics/default.png')  # Add a default image if none exists
    
    return render_template('account.html', title="Account", img_file=img_file, form=form)
