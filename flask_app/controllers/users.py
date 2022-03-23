import re
from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.register_user(data)
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id" : session['user_id']
    }
    logged_in_user = User.get_user_by_id(data)
    return render_template("dashboard.html", user = logged_in_user, recipes = Recipe.get_all())

@app.route('/login', methods = ['POST'])
def login():
    user = User.validate_email(request.form)
    if not user:
        flash('Invalid login credentials','login')
        return redirect ('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash ('Invalid login credentials', 'login')
        return redirect ('/')
    session['user_id'] = user.id 
    return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    