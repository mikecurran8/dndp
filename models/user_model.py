from db_utils import execute_query, execute_query_with_result
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def get_hashed_password(username):
    query = "SELECT password FROM users WHERE username = %s"
    result = execute_query_with_result(query, (username,))[0][0]
    print(f"query results are: {result}")
    if result is None:
        return False # No password found
    return result 

def insert_user(first_name, last_name, username, password):
    if username_exists(username):
        return None

    hashed_password = hash_password(password)
    query = "INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)"
    params = (first_name, last_name, username, hashed_password)
    execute_query(query, params)
    user_id = execute_query_with_result("SELECT id FROM users WHERE username = %s", (username,))[0]
    return user_id

def username_exists(username):
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    result = execute_query_with_result(query, (username,))[0]
    return result > 0

def verify_user_credentials(username, password):
    stored_hashed_password = get_hashed_password(username)
    if stored_hashed_password is None:
        return False # User not found or no password set

    user_id = execute_query_with_result("SELECT id FROM users WHERE username = %s", (username,))[0][0]
    return user_id
