import streamlit as st
from auth import verify_user

def render_login(go):
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            ok, msg = verify_user(username, password)
            if ok:
                st.success(msg)
                st.session_state.logged_in = True
                st.session_state.user_name = username
                st.rerun()
            else:
                st.error(msg)

    with col2:
        if st.button("Back to Sign Up"):
            go("signup")