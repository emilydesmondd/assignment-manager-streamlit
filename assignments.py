import streamlit as st


st.markdown("# Add new assignment")

text_input = st.text_input("Assignment Name")
st.write('Title', placeholder="e.g. Homework 1")

description_input = st.text_area("Description")
st.write('Description', placeholder="e.g. This assignment covers chapters 1-3.")
assignment_type_input = st.selectbox("Assignment Type", ["Homework", "Project", "Exam"])
st.radio('Assignment Type', placeholder="e.g. Homework")
if assignment_type_input == 'Other':
    assignment_type_input = st.text_input("Please specify assignment type")
due_date_input = st.date_input("Due Date")

