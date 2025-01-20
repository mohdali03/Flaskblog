
from flask import render_template,flash, redirect, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.user.form import (SignUpForm, LoginForm,
                    UpdateAccountForm, 
                    RequestRestForm, ResetPasswordForm)
from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.user.utils import save_picture, send_resetEmail
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users',__name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
       
        hashpassword = generate_password_hash(form.password.data) # type: ignore    
        user = User(username=form.username.data, email=form.email.data, password=hashpassword)# type: ignore
        # print(user)
        db.session.add(user)
        db.session.commit()
        
        flash(f"Acccount Created for {form.username.data}!", 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

            
        if user and check_password_hash(user.password, form.password.data): # type: ignore
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            flash(f"login Success! Welcome, {user.username}!", "success" )
            print(next_page)
            return redirect(next_page) if next_page and next_page.startswith('/') else redirect(url_for('main.home'))
        elif not user:
            flash(f"You don't Have Account! Register first", 'danger')
            return redirect(url_for('users.register'))
        else:
            flash(f"Login UnsuccessFull. Please check email & password", 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")

    return redirect(url_for('main.home'))


@users.route("/user/<string:username>")
def user(username):
    page= request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.datePosted.desc()).paginate(page=page,per_page=3)
    # print(user_post)
    return render_template('user.html', title="User Post", posts=posts, user=user)



@users.route("/reset_password", methods =['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_resetEmail(user)
        flash("An Email has been sent with intructions to reset your password", 'success')
        return redirect(url_for('users.login'))
        
    return render_template('rest_request.html', title='Reset Password', form = form)


@users.route('/rest_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
    
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    form = ResetPasswordForm()
    if user is None:
        flash("that is an invalid Token or expired token", 'warning')
        return redirect(url_for('users.reset_request'))
    if form.validate_on_submit():
        hashpassword = generate_password_hash(form.password.data) #type:ignore
        user.password  = hashpassword
        db.session.commit()
        flash("You Password is successfull changed!", 'success')
        return redirect(url_for('users.login'))
    return render_template('resetoken.html', title='Reset Password',
                           form = form)


@users.route('/account', methods=['POST', 'GET'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Pre-fill the form with current user's data
        form.username.data = current_user.username
        form.email.data = current_user.email

    if current_user.img_file:
        img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    else:
        img_file = url_for('static', filename='profile_pics/default.png')  # Add a default image if none exists
    
    return render_template('account.html', title="Account", img_file=img_file, form=form)

