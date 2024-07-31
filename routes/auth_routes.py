from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import insert_user, username_exists, verify_user_credentials

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_id = verify_user_credentials(username, password)
        if user_id:
            session['user_id'] = user_id
            flash('Login successful!', 'success')
            return redirect(url_for('character_bp.character_management'))
        else:
            flash('Invalid username or password', 'error')
    
    from app import prepare_main_content
    home_content = prepare_main_content()
    return render_template('index.html', home_content=home_content)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        
        if username_exists(username):
            flash('Username already exists', 'error')
        else:
            user_id = insert_user(first_name, last_name, username, password)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

