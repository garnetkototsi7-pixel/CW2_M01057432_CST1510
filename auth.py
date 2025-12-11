import bcrypt
import os

# --- Configuration ---
USER_DATA_FILE = "users.txt"

# --- Security Functions ---

def hash_password(plain_text_password):
    """
    Hashes a plain-text password using bcrypt.
    """
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    # gensalt() generates a random salt for security
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    # The result contains the cost, the salt, and the hash.
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plain-text password against a stored bcrypt hash.
    """
    # TODO: Encode both the plaintext password and the stored hash to byte
    password_bytes = plain_text_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    
    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hash_bytes)
    
# --- User Management Functions ---

def user_exists(username):
    """
    Checks if a username already exists in the user data file.
    
    FIXED: Includes a check for empty/malformed lines to prevent ValueError.
    """
    # Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
        
    # Read the file and check each line for the username
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            line = line.strip() # Clean the line (remove newline and whitespace)
            
            # CRITICAL FIX: Ensure the line is not empty AND contains the separator
            if line and ',' in line:
                try:
                    # Safely unpack the values
                    user, hash_data = line.split(',', 1) 
                    if user == username:
                        return True
                except ValueError:
                    # Optionally log the malformed line, but skip it
                    continue
            
    return False

def register_user(username, password):
    """
    Registers a new user by hashing their password and saving credentials to file.
    """
    # Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' is already registered.")
        return False
        
    # Hash the password
    hashed = hash_password(password) 
    
    # Append the new user to the file
    # Format: username,hashed_password
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")
    
    print(f"User '{username}' registered successfully.")
    return True

def login_user(username, password):
    """
    Attempts to log in a user by verifying the provided password against the stored hash.
    
    FIXED: Includes a check for empty/malformed lines to prevent ValueError.
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    # Search for the username in the file
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            line = line.strip()
            
            # CRITICAL FIX: Ensure the line is not empty AND contains the separator
            if not (line and ',' in line):
                continue # Skip this line if it's empty or malformed
            
            try:
                # Safely unpack the values
                user, hash_data = line.split(',', 1)
            except ValueError:
                # Optionally log the malformed line, but skip it
                continue
                
            # Note: strip is often unnecessary here if line.strip() was done above,
            # but is harmless if you want to be extra safe against internal whitespace.
            # user = user.strip() 
            # hash_data = hash_data.strip()

            # If username matches, verify the password
            if user == username:
                if verify_password(password, hash_data):
                    print(f"Welcome back {user}!")
                    input("\nPress Enter to log out and return to the main menu...")
                    return True
                else:
                    print("Incorrect password.")
                    return False

    # Username not found
    print("Error: Username not found.")
    return False

# --- Validation and UI Functions (Placeholders) ---

# These are placeholders; you can implement your actual validation logic here.
def validate_username(username):
    """Placeholder for complex username validation."""
    return True, ""
    
def validate_password(password):
    """Placeholder for complex password validation."""
    return True, ""

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

# --- Main Program Logic ---

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
            
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                # Login function already handles success message and input pause
                pass 
            else:
                # Login function handles failure message, but an extra one here for clarity
                print("\nLogin failed. Please check your username or password.")

        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()