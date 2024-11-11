from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, disable_autonaming=True)

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./123.db'
    app.secret_key = 'KEY'
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from models import User
    
    @login_manager.user_loader
    def login_user(id):
        return User.query.get(id)
    
    @login_manager.unauthorized_handler
    def unathorized_callback():
        return redirect(url_for('home.html'))
    
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    migrate = Migrate(app, db, compare_type=True)
    
    return app
    