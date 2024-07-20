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

def login():
    st.title("Login Page")

    # User input for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_password = hash_password(password)
        user = users_collection.find_one({"username": username, "password": hashed_password})

        if user:
            st.success("Login successful!")
            st.switch_page("pages/Home.py")
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    login()