from flask import Flask as Fl
from flask_sqlalchemy import SQLAlchemy 
from .config import Config
from flask_login import LoginManager


from flask_marshmallow import Marshmallow 


db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()



def createApp():
    app = Fl(__name__, template_folder="template", static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    with app.app_context():
        from . import route, models
        # login_man
        # db.drop_all()
        db.create_all()
    return app