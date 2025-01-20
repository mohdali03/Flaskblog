from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user 
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
import imghdr
