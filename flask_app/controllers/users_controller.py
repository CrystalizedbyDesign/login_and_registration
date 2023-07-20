from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import Registration 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re 


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not Registration.validate_registration(request.form):
        return redirect('/')

    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    # Save the data without storing the result
    id = Registration.save(data)
    # Rest of the code remains the same
    session['ninja_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    
    ninja_in_db = Registration.get_by_email(request.form)
    # ninja is not registered in the db
    if not ninja_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(ninja_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['ninja_id'] = ninja_in_db.id
    session['first_name'] = ninja_in_db.first_name
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if not 'ninja_id'  in session:
        return redirect ('/logout')
    data = {
        'id': session['ninja_id']
    }
    return render_template('dashboard.html', ninja_in_db=Registration.get_by_login_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

