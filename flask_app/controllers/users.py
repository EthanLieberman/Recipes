# controller.py
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)




@app.route('/')
@app.route('/<none>')
def index(none=None):
    return render_template('index.html')




@app.route('/registration', methods=['POST'])
def registration():
    if not User._validate_registration(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    hashword = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashword
    }

    id = User.save(data)
    session['name'] = request.form['first_name']
    session['id'] = id
    return redirect('/dashboard')




@app.route('/login',methods=['post'])
def login():

    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid email/password",'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password", 'login')
        return redirect('/')

    
    session['name'] = user_in_db.first_name
    session['id'] = user_in_db.id

    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/dashboard')
def dashboard():
    print(session)
    if not session:
        return redirect('/')

    recipe = Recipe.getAll_recipe()

    currentuser = {
        'id': session['id']
    }

    user = User.get_one(currentuser)
    return render_template('dashboard.html', recipehtml = recipe, user = user)