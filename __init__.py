from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from dotenv import load_dotenv
import os
import secrets

# load_dotenv()

app =  Flask(__name__, static_folder='static',)
app.secret_key = 'your_secret_ktyhioey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fantastic25'
app.config['MYSQL_DB'] = 'your_database'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from .routes import main as main_blueprint
app.register_blueprint(main_blueprint)