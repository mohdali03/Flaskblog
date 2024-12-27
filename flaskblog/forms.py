from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user 
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
import imghdr
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confrim Password', validators=[DataRequired(), EqualTo('password')])
    # pass
    submit = SubmitField("Sign up")
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("This Username is Taken. Please choose a diffrenet")
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("This email is Taken. Please choose a diffrenet")
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_picture(self, picture):
        if picture.data:
            filename = secure_filename(picture.data.filename)
            file_type = imghdr.what(picture.data)
            if file_type not in ['jpeg', 'jpg', 'png']:
                raise ValidationError("Invalid file type! Please upload a valid image (PNG,JPG, JPEG) format")
            
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    # pass
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")
    