import hvac

def get_db_credentials():
    # Initialize the Vault client
    client = hvac.Client(url='http://192.168.7.44:8200')
    client.token = 'hvs.Z7aVfUBXlUa2tFMkKkV5okbT'  # Replace with your actual token or secure method to retrieve it
    
    # Read the secret from Vault
    secret = client.secrets.kv.v2.read_secret_version(path='dnd')
    credentials = secret['data']['data']
    
    return credentials

def main():
    # Retrieve credentials
    credentials = get_db_credentials()
    
    # Output credentials
    print("Database Credentials:")
    print(f"Host: {credentials['host']}")
    print(f"User: {credentials['user']}")
    print(f"Password: {credentials['password']}")
    print(f"Database: {credentials['database']}")

if __name__ == '__main__':
    main()

