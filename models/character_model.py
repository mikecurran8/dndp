from db_utils import execute_query, execute_query_with_result

def insert_character(user_id, name, speed):
    query = "INSERT INTO characters (user_id, name, speed) VALUES (%s, %s, %s)"
    params = (user_id, name, speed)
    execute_query(query, params)
    character_id = execute_query_with_result("SELECT id FROM characters WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))[0]
    return character_id

def get_characters_by_user_id(user_id):
    query = "SELECT id, name, speed FROM characters WHERE user_id = %s"
    characters = execute_query_with_result(query, (user_id,))
    print(f"query output is : {characters}")
    return characters

def get_character_details( character_id):
    query = "SELECT id, name, speed FROM characters where id = %s"
    character = execute_query_with_result(query, (character_id,))
    if character:
        return character[0]
    return None

def update_character(character_id, new_name, new_speed):
    query = "UPDATE characters SET name = %s, speed = %s WHERE id = %s"
    execute_query(query, (new_name, new_speed, character_id))

