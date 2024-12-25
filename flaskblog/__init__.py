from flask import Flask as Fl, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from .config import Config


from flask_marshmallow import Marshmallow 


db = SQLAlchemy()
ma = Marshmallow()



def createApp():
    app = Fl(__name__, template_folder="template", static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        from . import route, models
        db.create_all()
    return app