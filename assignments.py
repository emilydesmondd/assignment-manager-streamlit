import streamlit as st

st.header("Assignment Manager")

st.markdown("### Add New Assignment")

# Assignment name
text_input = st.text_input("Assignment Name", placeholder="e.g. Homework 1")

# Description
description_input = st.text_area(
    "Description",
    placeholder="e.g. This assignment covers chapters 1–3."
)

# Assignment type
assignment_type_input = st.selectbox(
    "Assignment Type",
    ["Homework", "Project", "Exam", "Other"]
)

# If Other selected
if assignment_type_input == "Other":
    assignment_type_input = st.text_input("Please specify assignment type")

# Due date
due_date_input = st.date_input("Due Date")

with st.expander("Assignment Details", expanded=True):
    st.markdown("### Live Preview")
    st.markdown(f"**Assignment Name:** {text_input}")
    st.markdown(f"**Description:** {description_input}")
    st.markdown(f"**Type:** {assignment_type_input}")
    st.markdown(f"**Due Date:** {due_date_input}")