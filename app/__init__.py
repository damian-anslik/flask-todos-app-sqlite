from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import logging

from .config import Config

db = SQLAlchemy()
mail = Mail()
sender = Config.MAIL_USERNAME

def setup_app_file_logger(app: Flask):
    logging.basicConfig(
        filename=Config.LOG_FILE,
        format=Config.LOG_FORMAT,
        encoding="utf-8",
        level=app.config["ENV"] == "development" and logging.DEBUG or logging.INFO,
    )
    app.logger.info("Logger created")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_app_file_logger(app)

    mail.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(int(user_id))

    from .blueprints import auth_blueprint, main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    app.logger.info("App created")

    return app
