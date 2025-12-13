import bcrypt 
import sqlite3
import pandas as pd 
from pathlib import Path


from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user


def register_user(username, password, role="user"):
    """
    Register a new user in the database.
    
    Args:
        username: User's login name
        password: Plain text password (will be hashed)
        role: User role (default: 'user')
        
    Returns:
        tuple: (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')
    
   
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()
    
    return True, f"User '{username}' registered successfully!"
    
def login_user( username, password):
    """
    Authenticate a user against the database.
    
    Args:
        username: User's login name
        password: Plain text password to verify
        
    Returns:
        tuple: (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return False, "Username not found."
    
    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."

def migrate_users_from_file(conn,filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    migrated_count = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) >= 3 else "user"
                
               
                try: 
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    return migrated_count



def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table
        
    Returns:
        int: Number of rows loaded
    """
   
    if not Path(csv_path).exists():
        print(f"\nError: CSV file not found at {csv_path}")
        return 0

    try:
        df = pd.read_csv(csv_path)

        cursor = conn.cursor()
      
        cursor.execute(f"PRAGMA table_info({table_name})")
        print(f"\nTable {table_name} schema:", cursor.fetchall())
        print(f"\nCSV Columns found: {df.columns.tolist()}") 
        # ---------------------------------------------------------
            
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        conn.commit()

        
        row_count = len(df)
        return row_count
        
    except Exception as e:
        print(f"\nError loading csv into table ({table_name}: Data error: {e})")
        if 'df' in locals():
            print(f"\nCSV Columns found: {df.columns.tolist()}")
        return 0


if __name__ == "__main__":
    
    conn = connect_database()
    cursor = conn.cursor()

  
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)

    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

    print(f"\nTotal users: {len(users)}")
    conn.close()