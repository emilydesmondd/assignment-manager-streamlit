import streamlit as st

def render_homepage():
    st.title("Homepage")
    st.write(f"Welcome, **{st.session_state.user_name}**!")

    st.markdown("### Add a connection")

    name = st.text_input("Name")
    email = st.text_input("Email")
    company = st.text_input("Company")
    notes = st.text_area("Notes")

    if st.button("Add Connection"):
        if name:
            st.session_state.connections.append({
                "name": name,
                "email": email,
                "company": company,
                "notes": notes
            })
            st.success(f"Added {name}!")

    st.markdown("### Your connections")

    for i, c in enumerate(st.session_state.connections, 1):
        st.write(f"**{i}. {c['name']}**")
        if c["company"]:
            st.write("Company:", c["company"])
        if c["email"]:
            st.write("Email:", c["email"])
        if c["notes"]:
            st.write("Notes:", c["notes"])
        st.divider()

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
