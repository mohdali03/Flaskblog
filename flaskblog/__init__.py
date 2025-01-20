from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from .config import Config


# Extensions initialized here
db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder="template", static_folder="static")
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from flaskblog.user.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()  # Create database tables
    return app
