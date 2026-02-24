import streamlit as st

st.title("Build your Network")
st.header("Create an account!")
st.write("Start building your network today!")

user_name = st.text_input("Enter your username", "John Doe")
user_password = st.text_input("Enter your password", type="password")
user_email = st.text_input("Enter your email address")

checkbox_state = st.checkbox('Would you like to join our email list?')
if checkbox_state:
    st.write('Thanks for subscribing to our email list!')

credentials = {
    "username": user_name,
    "password": user_password,
    "email": user_email
}

if st.button("Create Account"):
    st.success("Account created!")
    st.write("Welcome, " + user_name + "!")




