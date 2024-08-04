from flask_login import UserMixin
from . import mysql, bcrypt

class User(UserMixin):
    def __init__(self, id, username,  email, password, matricNumber=None,):
        self.id = id
        self.username = username
        self.matricNumber = matricNumber
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(user[0], user[1], user[2], user[3])
    
    @staticmethod
    def find_by_username(username):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(user[0], user[1], user[2], user[3])
    
    @staticmethod
    def create(username, email, password,matricNumber=None):
        cursor = mysql.connection.cursor()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute('INSERT INTO users (username, matricNumber, email, password) VALUES (%s, %s, %s, %s)', (username, matricNumber, email, hashed_password))
        mysql.connection.commit()
        return cursor.lastrowid
