import streamlit as st
from project.auth import init_db, create_user
from project.login import render_login
from project.homepage import render_homepage

st.set_page_config(page_title="Network Manager", layout="wide")

init_db()

st.markdown("# 🤝 Network Manager")
st.markdown("Turn conversations into connections.")
st.markdown("---")

# session defaults
if "view" not in st.session_state:
    st.session_state.view = "signup"   # signup | login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def go(view: str):
    st.session_state.view = view
    st.rerun()

# If logged in → show the real app (sidebar inside homepage.py)
if st.session_state.logged_in:
    render_homepage()
    st.stop()

# ---------- SIGNUP ----------
st.title("Build your Network")

if st.session_state.view == "signup":
    st.subheader("Create an account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account"):
            if not username or not email or not password:
                st.error("Please fill out username, email, and password.")
            else:
                ok, msg = create_user(username.strip(), email.strip(), password)
                if ok:
                    st.success(msg)
                    st.session_state.logged_in = True
                    st.session_state.user_name = username.strip()
                    st.session_state.user_email = email.strip()
                    st.rerun()
                else:
                    st.error(msg)

    with col2:
        if st.button("Already have an account? Login"):
            go("login")

# ---------- LOGIN ----------
elif st.session_state.view == "login":
    render_login(go)