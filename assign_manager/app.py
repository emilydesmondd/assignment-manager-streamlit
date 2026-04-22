
import streamlit as st

st.set_page_config(page_title="Assignement Manager")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'role' not in st.session_state:
    st.session_state['role'] = 'Instructor'

if 'page' not in st.session_state:
    st.session_state['page'] = 'Dashboard'

if st.session_state['logged_in']:
    if st.session_state['role'] == 'Instructor':
        pass
    elif st.session_state['role'] == 'Student':
        pass
else:
    pass
#set up log in register page


