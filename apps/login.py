import streamlit as st
from apps.auth import verify_user, get_user_email

def render_login(go):
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if not username or not password:
                st.error("Please enter your username and password.")
            else:
                username_clean = username.strip()
                ok, msg = verify_user(username_clean, password)

                if ok:
                    st.success(msg)
                    st.session_state.logged_in = True
                    st.session_state.user_name = username_clean
                    st.session_state.user_email = get_user_email(username_clean) or ""
                    st.rerun()
                else:
                    st.error(msg)

    with col2:
        if st.button("Back to Sign Up"):
            go("signup")