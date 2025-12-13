import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_datasets_metadata(dataset_id, name, rows, columns, uploaded_by, upload_date):
    """Insert new dataset record."""
    try:
        conn = connect_database()
        cursor = conn.cursor()
        insert_sql = """
                   INSERT INTO datasets_metadata
                   (dataset_id, name, rows, columns, uploaded_by, upload_date )
                   VALUES (?, ?, ?, ?, ?, ?)
                   """ 
        cursor.execute(
            insert_sql,
            (dataset_id, name, rows, columns, uploaded_by, upload_date)
        )         
        conn.commit()  
        
        return cursor.lastrowid
    
    except Exception as e:
        print(f"Error inserting dataset: {e}")
        return None
    
def get_all_datasets_metadata(conn):
    """
    Retrieve all dataset metadata records.
    ARGS:
    conn: Database connection object
    Returns: pandas.DataFrame: All dataset metadata
    """
    try:
        conn = connect_database()
        df = pd.read_sql_query(
            "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC", 
            conn)
        conn.close()
        return df
    
    except Exception as e:
        print(f"Error retrieving datasets: {e}")
        return pd.DataFrame()
    
def update_datasets_metadata(conn, id, name=None, last_updated=None, source=None):
    """
    Update dataset metadata fields
    """
    try:
        cursor = conn.cursor()
        if name is not None:
            cursor.execute("UPDATE datasets_metadata SET name=? WHERE id=?", (name, id))
        if last_updated is not None:    
            cursor.execute("UPDATE datasets_metadata SET last_updated=? WHERE id=?", (last_updated, id))
        if source is not None:    
            cursor.execute("UPDATE datasets_metadata SET source=? WHERE id=?", (source, id))
        
        conn.commit()
        return cursor.rowcount
   
    except Exception as e:
        print(f"Error updating dataset metadata: {e}")
        return 0
    

def delete_datasets_metadata(conn, id):
    """
    Delete a dataset metadata record
    Args:
    conn: Database connection object
    dataset_id(int): ID of the dataset to delete
      """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE  FROM datasets_metadata WHERE id=?", (id,))
        conn.commit()
        print("Dataset metadata deleted successfully!")
        return cursor.rowcount

    except Exception as e:
        print(f"Error deleting dataset metadta: {e}")