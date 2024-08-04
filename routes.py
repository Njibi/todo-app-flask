from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, mysql, bcrypt
from . import mysql, bcrypt 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        matricNumber = request.form['matricNumber']
        email = request.form['email']
        password = request.form['password']
        
        user = User.find_by_username(username)
        if user:
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        user_id = User.create(username, matricNumber, email, password)
        flash('you have sucessfully registered', 'sucess')
        user = User.get(user_id)
        login_user(user)
        return redirect(url_for('main.dashboard'))
    
    return render_template('/index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.find_by_username(username)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid credentials')
        return redirect(url_for('main.login'))
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (current_user.id,))
    tasks = cursor.fetchall()
    return render_template('todo.html', tasks=tasks)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        # description = request.form['description']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tasks (title,  user_id) VALUES (%s,  %s)', (title,  current_user.id))
        mysql.connection.commit()
        return redirect(url_for('main.dashboard'))
    
    return render_template('todo.html')

@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = %s AND user_id = %s', (task_id, current_user.id))
    task = cursor.fetchone()
    if not task:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        cursor.execute('UPDATE tasks SET title = %s, description = %s WHERE id = %s', (title, description, task_id))
        mysql.connection.commit()
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_task.html', task=task)

@main.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, current_user.id))
    mysql.connection.commit()
    return redirect(url_for('main.dashboard'))
