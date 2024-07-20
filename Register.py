
import streamlit as st
from pymongo import MongoClient
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster_address = os.getenv("MONGODB_CLUSTER_ADDRESS")
dbname = os.getenv("MONGODB_DBNAME")

# Construct the MongoDB URI
MONGODB_URI = f"mongodb+srv://{username}:{password}@{cluster_address}/{dbname}?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URI)
    db = client[dbname]
    users_collection = db["users"]
except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Streamlit registration page
st.set_page_config(initial_sidebar_state="collapsed")   
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
st.title("Register Page")

# User input for new registration
new_username = st.text_input("New Username")
new_password = st.text_input("New Password", type="password")

if st.button("Register"):
    if new_username and new_password:
        if users_collection.find_one({"username": new_username}):
            st.error("Username already exists. Please choose another one.")
        else:
            hashed_password = hash_password(new_password)
            users_collection.insert_one({"username": new_username, "password": hashed_password})
            st.success("User registered successfully!")
            st.switch_page("pages/Login.py")
    else:
        st.error("Please provide a username and password")