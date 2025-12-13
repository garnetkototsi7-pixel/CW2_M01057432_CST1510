import pandas as pd
from pathlib import Path
from app.data.db import connect_database


def insert_it_tickets(priority,status, category, assigned_to, created_at):
    """Insert new dataset record."""
    try:
        conn = connect_database()
        cursor = conn.cursor() 
        insert_sql ="""
         INSERT INTO it_tickets
         (priority, status, category, assigned_to, created_at)
          VALUES (?, ?, ?, ?, ?)
          """
        cursor.execute(
            insert_sql,
            (priority, status, category, assigned_to, created_at)
        )
        conn.commit()

        
        
        return cursor.lastrowid
    
    except Exception as e:
        print(f"Error inserting ticket: {e}")
        return None
    
def get_all_it_tickets(conn):
    """
    Load all IT tickets from the csv file.
    Returns: pd.DataFrame: All ticket records sorted by ticket_id descending
    """
    try:
        conn = connect_database()
        df = pd.read_sql_query(
            "SELECT  * FROM it_tickets ORDER BY ticket_id DESC", 
            conn
            )
        conn.close()
        return df 

    except Exception as e:
        print(f"Error retrieving IT tickets: {e}")
        return pd.DataFrame()
    
def delete_it_tickets(conn, ticket_id):
    """
    Delete a ticket by ID
    """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE  FROM it_tickets WHERE id=?", (ticket_id,))
        conn.commit()
        print("IT ticket deleted successfully!")
        return cursor.rowcount

    except Exception as e:
        print(f"Error deleting ticket: {e}")

def update_it_tickets(conn, ticket_id, priority=None, description=None, status=None, assigned_to=None, created_at=None):
    """
    Update fields of a ticket. Only updates field that are not None.
    """
    try:
        cursor = conn.cursor()
       
        if priority is not None:
            cursor.execute("UPDATE it_tickets SET priority=? WHERE id=?", (priority, ticket_id))
        if description is not None:
            cursor.execute("UPDATE it_tickets SET description=? WHERE id=?", (description, ticket_id))
        if status is not None:
            cursor.execute("UPDATE it_tickets SET status=? WHERE id=?", (status, ticket_id))
        if assigned_to is not None:
            cursor.execute("UPDATE it_tickets SET assigned_to=? WHERE id=?", (assigned_to, ticket_id))
        if created_at is not None:
            cursor.execute("UPDATE it_tickets SET created_at=? WHERE id=?", (created_at, ticket_id))

        conn.commit()
        return cursor.rowcount
            
        
    except Exception as e:
        print(f"Error updating ticket: {e}")
        return False
  
