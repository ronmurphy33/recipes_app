import re
from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes/new')
def create_recipe():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template('new_recipe.html')

@app.route('/recipes/save', methods = ['POST'])
def save():
    if 'user_id' not in session:
        return redirect ('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data ={
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "time_length" : int(request.form['time_length']),
        "recipe_date": request.form['recipe_date'],
        "user_id": session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def display_recipe(id):
    if 'user_id' not in session: 
        return redirect('/')
    data = {
        "id" : id
    }
    active_user = {
        "user_id": session['user_id']
    }
    return render_template('recipe.html', recipe = Recipe.get_one(data), user =User.get_user_by_id(active_user))

@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    if 'user_id' not in session: 
        return redirect('/')
    data = {
        "id" : id
    }
    return render_template('edit_recipe.html', recipe = Recipe.get_one(data))

@app.route('/recipes/update', methods = ['POST'])
def update_recipe():
    if 'user_id' not in session: 
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "time_length" : int(request.form['time_length']),
        "recipe_date": request.form['recipe_date'],
        "id":request.form['id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def destroy_recipe(id):
    data = {
        "id": id
    }
    Recipe.destroy_recipe(data)
    return redirect('/dashboard')

