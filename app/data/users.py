from app.data.db import connect_database
def get_user_by_username(conn, username):
    """Retrieve user by username"""
    cursor = conn.cursor()
    conn = connect_database()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    
    return cursor.fetchone() 
    
def insert_user(conn, username, password_hash, role='user'):
    """Insert new user."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
        (username, password_hash, role)
    )
    conn.commit()
    