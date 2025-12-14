import streamlit as st
import os
import bcrypt

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# --- Initialize session state ---
if "users" not in st.session_state:
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        username, hashed_password = line.split(",", 1)
                        users[username.strip()] = hashed_password.strip()
                    except ValueError:
                        st.error(f"Skipping badly formatted line: '{line}'")
                        continue
    st.session_state.users = users

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --- User functions ---
def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    st.session_state.users[username] = hashed.decode()
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed.decode()}\n")

def login_user(username, password):
    if username not in st.session_state.users:
        return False
    hashed = st.session_state.users[username].encode()
    return bcrypt.checkpw(password.encode(), hashed)

# --- Already logged in ---
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Go to dashboard"):
            st.switch_page("Pages/1_Dashboard.py")  
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    st.stop()

# --- Login / Register Tabs ---
st.title("Welcome Lads")
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not login_username or not login_password:
            st.error("Please enter both username and password")
        elif login_user(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Logged in as {login_username}")
            st.rerun()
        else:
            st.error("Invalid username or password")

with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    
    if st.button("Register"):
        if not new_username or not new_password or not confirm_password:
            st.error("All fields are required")
        elif len(new_username) < 3 or len(new_username) > 20 or not new_username.isalnum():
            st.error("Username must be 3-20 alphanumeric characters")
        elif len(new_password) < 6 or len(new_password) > 50:
            st.error("Password must be 6-50 characters")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        elif new_username in st.session_state.users:
            st.error("Username already exists")
        else:
            register_user(new_username, new_password)
            st.success("Registration successful! You can now log in.")
