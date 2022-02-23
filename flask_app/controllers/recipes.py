# controller.py
from contextlib import nullcontext
from tarfile import NUL

from pymysql import NULL
from flask_app import app
from flask import render_template, redirect, request, session, flash
import flask_app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from datetime import datetime

date_format = "%m/%d/%Y %I:%M %p"


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html')


@app.route('/create_recipe',methods=['post'])
def create_recipe():
    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False

    if len(request.form['description']) < 1:
        is_valid = False

    if len(request.form['instructions']) < 1:
        is_valid = False

    # if request.form['under30'] == NUL:
    #     is_valid = False

    if not is_valid:
        flash("na chef cant leave any info out", "recipe")
        return redirect('/new_recipe')
    
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': request.form['under30'],
        'users_id': session['id'],

    }
    Recipe.new_recipe(data)
    return redirect('/dashboard')



@app.route('/view_recipe/<int:id>')
def recipe(id):
    recipefrompage = {
        'id': id
    }

    recipeid = Recipe.get_one(recipefrompage)


    currentuser = {
        'id': session['id']
    }

    user = User.get_one(currentuser)

    return render_template('recipe.html', recipeid = recipeid, user = user, date_format=date_format)


@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    recipefrompage = {
        'id': id
    }

    recipeid = Recipe.get_one(recipefrompage)

    return render_template('recipe_edit.html', recipeid = recipeid)


@app.route('/update_recipe',methods=['post'])
def update_recipe():
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': request.form['under30'],
        'users_id': session['id']
    }
    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False

    if len(request.form['description']) < 1:
        is_valid = False

    if ('under30' in data and data['under30'] not in ['yes','no']):
        is_valid = False

    if len(request.form['instructions']) < 1:
        is_valid = False
    
    if not is_valid:
        flash("na chef cant leave any info out", "recipe")
        recipeid = data['id']
        return redirect(f'/edit_recipe/{recipeid}')



    
    Recipe.update_recipe(data)

    return redirect('/dashboard')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):

    recipefrompage = {
        'id': id
    }

    Recipe.delete_recipe(recipefrompage)

    return redirect('/dashboard')


