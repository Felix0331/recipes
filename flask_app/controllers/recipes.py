from flask import render_template,request,redirect,session,flash
from werkzeug import datastructures
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/success')
def success():
    if not session:
        flash("Please login")
        return redirect('/')
    recipes = Recipe.get_all()
    return render_template('dashboard.html',recipes = recipes)

@app.route('/add_recipe')
def render_add_recipe():
    if not session:
        flash("Please login")
        return redirect('/')
    return render_template('add_recipe.html')


@app.route('/create_new', methods = ['POST'])
def create_new():
    data={
        'name':request.form['name'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made'],
        'under_30_minutes':request.form['under_30_minutes'],
        'user_id':session['user_id']
    }
    Recipe.add_recipe(data)
    return redirect('/success')

@app.route('/recipes/edit/<int:recipe_id>')
def get_recipe(recipe_id):
    data={
        'id':recipe_id
    }
    recipe = Recipe.get_recipe(data)
    if session['user_id'] != recipe[0]['user_id']:
        flash("What are you trying to pull MF!?")
        return redirect('/')
    return render_template('edit_recipe.html',recipe = recipe)

@app.route('/edit_recipe/<int:recipe_id>', methods = ['POST'])
def edit_recipe(recipe_id):
    data={
        'id': recipe_id,
        'name':request.form['name'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made'],
        'under_30_minutes':request.form['under_30_minutes'],
        'user_id':session['user_id']
    }
    Recipe.edit_recipe(data)
    return redirect('/success')

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'id':recipe_id
    }
    recipe = Recipe.get_recipe(data)
    return render_template('show_recipe.html',recipe = recipe)

@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data={
        'id':recipe_id
    }
    recipe = Recipe.get_recipe(data)
    if session['user_id'] != recipe[0]['user_id']:
        flash("What are you trying to pull MF!?")
        return redirect('/')
    Recipe.delete_recipe(data)
    return redirect('/success')