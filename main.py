<<<<<<< HEAD
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.datasets_metadata import insert_datasets_metadata, get_all_datasets_metadata
from app.data.it_tickets import insert_it_tickets, get_all_it_tickets
from app.data.cyber_incidents import insert_incident, get_all_incidents
import sqlite3


from app.data.db import DB_PATH
from app.data.db import connect_database
def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
=======
from pathlib import Path
import sqlite3
from app.data.db import DB_PATH, connect_database, create_all_tables
from app.services.users_service import insert_user, get_user_by_username, migrate_users_from_file, load_csv_to_table
from app.data.datasets_metadata import insert_datasets_metadata, get_all_datasets_metadata
from app.data.it_tickets import insert_it_tickets, get_all_it_tickets
from app.data.incident import insert_incident, get_all_incidents


def setup_database_complete():
    """
    Complete database setup: Connect, Create tables, Migrate users, Load CSV data, and Verify.
>>>>>>> 3c9147c359203b49e5beea372354beee3adda199
    """
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)
<<<<<<< HEAD
    
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    from app.data.schema import create_all_tables
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")
    
    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    from app.services.user_service import load_csv_to_table
    total_rows = 0
    total_rows += load_csv_to_table(conn, 'DATA/datasets_metadata.csv', 'datasets_metadata')
    total_rows += load_csv_to_table(conn, 'DATA/it_tickets.csv', 'it_tickets')
    total_rows += load_csv_to_table(conn, 'DATA/cyber_incidents.csv', 'cyber_incidents')
    print(f" Loaded {total_rows} rows.")
    
    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"\n{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()
=======

    try:
        # Connect to DB
        with connect_database() as conn:
            print("\n[1/5] Connected to database.")

            # Step 2: Create tables
            print("\n[2/5] Creating database tables...")
            create_all_tables() 
            print("      Tables created successfully.")

            # Step 3: Migrate users
            print("\n[3/5] Migrating users from users.txt...")
            user_count = migrate_users_from_file(conn) 
            print(f"      Migrated {user_count} users")

            # Step 4: Load CSV data
            print("\n[4/5] Loading CSV data...")
            total_rows = 0

            BASE_DIR = Path(__file__).resolve().parent
            DATA_DIR = BASE_DIR.parent / "DATA"  # Ensure it points to the DATA folder

            # Load datasets_metadata.csv
            datasets_csv = DATA_DIR / "datasets_metadata.csv"
            it_tickets_csv = DATA_DIR / "it_tickets.csv"
            cyber_incidents_csv = DATA_DIR / "cyber_incidents.csv"

            total_rows += load_csv_to_table(conn, datasets_csv, "datasets_metadata")
            total_rows += load_csv_to_table(conn, it_tickets_csv, "it_tickets")
            total_rows += load_csv_to_table(conn, cyber_incidents_csv, "cyber_incidents")

            print(f"      Loaded {total_rows} rows.")

            # Step 5: Verify table contents
            print("\n[5/5] Verifying database setup...")
            cursor = conn.cursor()
            tables = ['users', 'datasets_metadata', 'cyber_incidents', 'it_tickets']
            print("\n Database Summary:")
            print(f"\n{'Table':<25} {'Row Count':<15}")
            print("-" * 40)
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:<25} {count:<15}")

        print("\n" + "=" * 60)
        print(" DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print(f"\n Database location: {DB_PATH.resolve()}")
        print("\nYou're ready for Week 9 (Streamlit web interface)!")

    except Exception as e:
        print(f"\nFATAL ERROR DURING SETUP: {e}")
        print("Please ensure your database file is accessible and all tables are defined.")


if __name__ == '__main__':
    setup_database_complete()
>>>>>>> 3c9147c359203b49e5beea372354beee3adda199
