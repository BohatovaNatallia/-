from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)


app.config.from_object('config')

db = SQLAlchemy(app, session_options={"autoflush": False})

with app.app_context():
    db.create_all()
    from app import views, model

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.get(int(user_id))


