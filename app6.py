import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Course Manager", layout="centered")
st.title("Course Manager Application")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "role" not in st.session_state:
    st.session_state["role"] = None

users = [
        {
        "id": "1",
        "email": "admin@school.edu",
        "full_name": "System Admin",
        "password": "123ssag@43AE",
        "role": "Admin",
        "registered_at": "..."
    }
]

if st.session_state["role"] == "Admin":
    st.markdown("This is the Admin UI- Dashboard")

    if st.button("Log Out"):
        with st.spinner("logging out..."):
            time.sleep(4)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()


elif st.session_state["role"] =="Instructor":
    st.markdown("This is the Instrcuctor Dashboard")

else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email Address", key = "email_address_login")
        password_input = st.text_input("Password", type="password", key = "password_login")
        
        if st.button("Log In", type="primary",use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
                
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"]= True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user['role']
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    st.subheader("New Instructor Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="email_address_register")
        new_password = st.text_input("Password", type="password" , key = "password_reg")
        
        if st.button("Create Account", type="secondary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Instructor"
                })
                #with open(json_file, "w") as f:
                #   json.dump(users, f, indent=4)
                st.success(f"Account created! {new_email}")
                time.sleep(4)
                st.rerun()

    st.write("---")
    st.dataframe(users)

with st.sidebar:
    if "logged_in" in st.session_state and st.session_state["logged_in"] != False:
        user = st.session_state["user"]
        st.markdown(f"Welcome {user['email']}")
    else:
        st.markdown("Welcome! - Login")
        