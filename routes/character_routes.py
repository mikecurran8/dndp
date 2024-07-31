from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.character_model import insert_character, get_characters_by_user_id, get_character_details, update_character

# Create a Blueprint for character routes
character_bp = Blueprint('character_bp', __name__)

@character_bp.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = session['user_id']
        name = request.form['name']
        speed = request.form['speed']
        character_id = insert_character(user_id, name, speed)
        
        if character_id:
            flash('Character created successfully!', 'success')
        else:
            flash('Failed to create character.', 'error')
        
        return redirect(url_for('character_bp.character_management'))

    return render_template('create_character.html')

@character_bp.route('/edit_character/<int:character_id>', methods=['GET', 'POST'])
def edit_character(character_id):
    if 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']

    if request.method == 'POST':
        new_name = request.form['name']
        new_speed = request.form['speed']
        update_character(character_id, new_name, new_speed)
        flash('Character successfully updated!', 'success')
        return redirect(url_for('character_bp.character_management'))
    
    character = get_character_details(character_id)

    from app import prepare_char_content
    character_content = prepare_char_content(character_id)
    return render_template('index.html', character_content=character_content)

@character_bp.route('/character/<int:character_id>', methods=['GET'])
def view_character(character_id):
    if 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    character = get_character_details(character_id)
    return render_template('view_character.html', character=character)

@character_bp.route('/character_management')
def character_management():
    if 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    #characters = get_characters_by_user_id(user_id)

    # Print output of query
    print(f"The output of the characters management route")

    from app import prepare_main_content
    home_content = prepare_main_content()
    return render_template('index.html', home_content=home_content)

