from flask import Flask, render_template, session, flash
from routes.auth_routes import auth_bp
from routes.character_routes import character_bp
from models.character_model import get_characters_by_user_id,get_character_details

app = Flask(__name__)
app.secret_key = 'LivingDead3!'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(character_bp, url_prefix='/characters')

def prepare_main_content():
    user_id = session.get('user_id')
    if user_id:
        characters = get_characters_by_user_id(user_id)
        characters_list = render_template("partials/characters_list.html", characters=characters)
    else:
        characters_list = "<p>You have not yet created any characters.</p>"

    home_content = render_template('partials/home.html', characters_list=characters_list)
    return home_content

def prepare_char_content(character_id=0):
    if character_id < 1:
        character_content=render_template("partials/characters.html", character_id=character_id)
    else:
        character = get_character_details(character_id)
        character_content = render_template("partials/characters.html", character=character, character_id=character_id)
    return character_content

@app.route('/')
def index():
    home_content = prepare_main_content()
    character_content = prepare_char_content()
    return render_template('index.html', home_content = home_content, character_content = character_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

