from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

db = SQLAlchemy()
DB_NAME = "database.db"

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=3600)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    # Enable CORS for the React frontend
    CORS(app)  # Add this line
    
    from .auth import auth  # Import auth blueprint
    app.register_blueprint(auth, url_prefix='/')
    from .routes import api  # Import api blueprint
    app.register_blueprint(api, url_prefix='/api')

    from .models import User, Note
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
