import hvac
import mysql.connector
from mysql.connector import errorcode

# Function to get database credentials from Vault
def get_db_credentials():
    client = hvac.Client(url='http://192.168.7.44:8200')
    client.token = 'hvs.Z7aVfUBXlUa2tFMkKkV5okbT'  # Replace with your actual token or method to retrieve it securely
    secret = client.secrets.kv.v2.read_secret_version(path='dnd')
    credentials = secret['data']['data']
    return credentials

def get_db_connection():
    credentials = get_db_credentials()
    return mysql.connector.connect(
        host=credentials['host'],
        user=credentials['user'],
        password=credentials['password'],
        database=credentials['database']
    )

def normalize_result(result):
    if result is None:
        return []
    if isinstance(result, tuple):
        return [result]
    return result

def execute_query(query, params=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn:
            conn.rollback()

def execute_query_with_result(query, params=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return normalize_result(result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
