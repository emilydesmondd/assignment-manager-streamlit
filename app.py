import streamlit as st
from auth import init_db, create_user
from login import render_login
from homepage import render_homepage

st.set_page_config(page_title="Network Manager", layout="centered")

init_db()

# Session defaults
if "view" not in st.session_state:
    st.session_state.view = "signup"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "connections" not in st.session_state:
    st.session_state.connections = []

def go(view):
    st.session_state.view = view
    st.rerun()

# If logged in → homepage
if st.session_state.logged_in:
    render_homepage()
    st.stop()

# ---------------- SIGNUP ----------------
if st.session_state.view == "signup":
    st.title("Build your Network")
    st.header("Create an account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account"):
            if not username or not email or not password:
                st.error("Fill out all fields.")
            else:
                ok, msg = create_user(username, email, password)
                if ok:
                    st.success(msg)
                    st.session_state.logged_in = True
                    st.session_state.user_name = username
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error(msg)

    with col2:
        if st.button("Already have an account? Login"):
            go("login")

# ---------------- LOGIN ----------------
elif st.session_state.view == "login":
    render_login(go)