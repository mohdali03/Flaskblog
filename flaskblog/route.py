import os
import secrets
# from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort

# from sqlalchemy import or_

from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post, db
from flask import current_app as app
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from . import mail



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

def send_resetEmail(user):
    
        token = user.get_reset_token()
        msg = Message("Password Reset Request", sender='noreply@demo.com',
                    recipients=[user.email])
        msg.html = f''' <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <title>Password Reset</title>
      </head>
      <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f7ff;">
        <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden;">
          <header style="background-color: #4CAF50; padding: 20px; text-align: center; color: white; font-size: 24px;">
            Password Reset Request
          </header>
          <main style="padding: 20px;  text-align: center;">
            <p style='text-align: center;' >Hi {user.username},</p>
            <p style='text-align: center;' >We received a request to reset your password. Click the link below to reset it:</p>
            <a href="{url_for('users.reset_token', token=token, _external=True)}" style="display: inline-block; margin: 20px 0; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; text-align: center;">Reset Password</a>
            <p>If you did not request this, please ignore this email and your password will remain unchanged.</p>
          </main>
          <footer style="background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px;">
            
            <p>&copy; 2024 Flask Blog. All rights reserved.</p>
          </footer>
        </div>
      </body>
    </html>
        '''

        mail.send(msg)
    

    # form = ResetPasswordForm()
    