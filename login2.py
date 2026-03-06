import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Course Manager", layout="centered")

json_file = Path("users.json")

if json_file.exists():
    with open(json_file, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = [
        {
            "id": "1",
            "email": "admin@school.edu",
            "first_name": "System",
            "last_name": "Admin",
            "password": "123ssag@43AE",
            "role": "Admin",
            "registered_at": '...'
        }
    ]
    with open(json_file, "w") as f:
        json.dump(users, f, indent=4)

st.title("Course Manager")

page = st.sidebar.radio("Choose a page", ["Register", "Login"])

if page == "Register":
    st.subheader("New Instructor Account")

    with st.container():
        email = st.text_input("Email Address")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Instructor"])

        if st.button("Create Account"):
            if not email or not first_name or not last_name or not password:
                st.error("Please fill out all fields.")
            else:
                email_exists = any(user["email"] == email for user in users)

                if email_exists:
                    st.error("An account with this email already exists.")
                else:
                    with st.spinner("Creating your account..."):
                        time.sleep(5)

                        new_user = {
                            "id": str(uuid.uuid4()),
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            "password": password,
                            "role": role,
                            "registered_at": str(datetime.now())
                        }

                        users.append(new_user)

                        with open(json_file, "w") as f:
                            json.dump(users, f, indent=4)

                    st.success("Account created successfully!")

elif page == "Login":
    st.subheader("Login")

    with st.container():
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")

        if st.button("Log In"):
            with st.spinner("Verifying credentials..."):
                time.sleep(5)

                matched_user = None
                for user in users:
                    if user["email"] == login_email and user["password"] == login_password:
                        matched_user = user
                        break

                if matched_user:
                    st.success(
                        f"Welcome back, {matched_user['first_name']}! "
                        f"Role: {matched_user['role']} | Email: {matched_user['email']}"
                    )
                else:
                    st.error("Invalid email or password.")

    st.subheader("Current User Database")
    st.dataframe(users)

#json_path = Path("users.json")
#if json_path.exists():
#    with open(json_path, "r", encoding="utf-8") as f:
#        users = json.load(f)