# app constructor file
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
# login protect view
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


# define create_app .create app and initialization expand,return program object
# flask-expand often init when create flask object
def create_app(config_name):
    # create flask object
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # HTML model to use bootstrap/base.html
    bootstrap.init_app(app)
    # send email
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # join blueprint include view function, main/views.py
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # auth/views.py
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # api_1_0/...py
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app
