import os
import secrets
# from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from datetime import datetime
# from sqlalchemy import or_
from .forms import SignUpForm, LoginForm,UpdateAccountForm, PostForm
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
'''
Title: "Mastering Python: Top 10 Beginner Tips"
Content:
Python is one of the easiest programming languages to learn. Start with understanding variables, loops, and functions. Explore libraries like NumPy and Pandas for data analysis.
Title: "The Power of SQL: Why Every Developer Should Learn It"
Content:
SQL is the backbone of managing data in modern applications. Learn about queries, joins, and how to optimize database performance to enhance your applications.
Title: "5 Quick Tips for Clean and Efficient Code"
Content:
Writing clean code is essential for collaboration. Use meaningful variable names, write modular functions, and always document your code for better readability.
Title: "The Role of Flask in Web Development"
Content:
Flask is a lightweight Python web framework perfect for building APIs and dynamic websites. Learn how to set up routes, templates, and handle requests efficiently.
Title: "Understanding RESTful APIs: A Beginner’s Guide"
Content:
RESTful APIs are the cornerstone of modern web applications. Learn about HTTP methods, status codes, and how to design scalable APIs for your projects.
Title: "Why Git and GitHub Are Essential for Developers"
Content:
Version control is crucial for developers. Learn the basics of Git, branching, and how to collaborate on projects using GitHub repositories.
Title: "Exploring JavaScript Frameworks: React vs Angular"
Content:
Both React and Angular are powerful tools for building interactive web applications. Compare their features, use cases, and decide which fits your project best.
Title: "Boost Your Productivity with VS Code Extensions"
Content:
Discover must-have VS Code extensions like Prettier for formatting, GitLens for version control, and Live Server for real-time web development.
Title: "Introduction to Machine Learning with Python"
Content:
Machine learning is transforming industries. Start with libraries like Scikit-learn and TensorFlow, and learn to create basic models for predictions and analysis.
Title: "How to Build a Blog App with Flask"
Content:
Learn to create a functional blog app using Flask. Cover topics like setting up routes, integrating a database, user authentication, and deploying your app online.
'''
@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page=2, page=page)
    for pagen in posts.iter_pages():  
        print(pagen)
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
        else:
            flash(f"Login UnsuccessFull. Please check email & password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")

    return redirect(url_for('home'))

def save_picture(form_picture):
 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
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

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # type:ignore
        flash("Your post has been created!", 'success')
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('newPost'))
    return render_template('createPost.html', title="New Post", form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def UpdatePost(post_id):
    post = Post.query.get_or_404(post_id)
    # return render_template("post.html", title=post.title, post=post)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has Been Update!", "success")
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET": 
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('createPost.html', title="Update Post", form=form, legend='Update Post')
    
@app.route('/DeletePost/<int:post_id>', methods = ['POST'])
def DeletePost(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "danger")
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user(username):
    page= request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.datePosted.desc()).paginate(page=page,per_page=3)
    # print(user_post)
    return render_template('user.html', title="User Post", posts=posts, user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404

