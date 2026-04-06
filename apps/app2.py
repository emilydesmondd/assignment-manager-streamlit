import streamlit as st

st.title("Course Management App")
st.header("Assignments")
st.subheader("Assignments Manager")

next_assignment_id_number = 3

st.divider()

#load assignments
assignments = [
    {
        "id" : "HW1",
        "title" : "Introduction to Database",
        "description": "basics of database design",
        "points" : 100,
        "type" : "homework"
    },
    {
        "id": "HW2",
        "title": "Normalization",
        "description" : "Normalize the table designs",
        "points": 100,
        "type" : "lab"
    }
]

# Add New Assignment
st.markdown("# Add New Assignment")

#input

title = st.text_input("Title",placeholder="ex. Homework 1", 
                      help="This is the name of the assignment")

description = st.text_area("Description",placeholder="ex. database design...")
due_date = st.date_input("Due Date")
assignments_type = st.radio("Type",["Homework", "Lab"])

points = st.number_input("Points")

#assignments_type2 = st.selectbox("Type", ["Homework", "Lab","Other"])
#if assignments_type2 == "Other":
 #   assignments_type2 = st.text_input("Assingment Type")

#lab = st.checkbox("Lab")

with st.expander("Assignment Preview",expanded= True):
    st.markdown("## Live Preview")
    st.markdown(f"Title: {title}")

btn_save = st.button("Save",use_container_width=True, disabled=False)

import time

import json
from pathlib import Path

json_path = Path("assignments.json")

if btn_save:
    with st.spinner("Saving the Assignmnet..."):
        time.sleep(5)
        if not title:
            st.warning("Enter Assignmnet Title")
        else:
            #Add/Create new Assignmnet
            new_assignmnet_id = "HW" + str(next_assignment_id_number)
            next_assignment_id_number += 1

            assignments.append(
                {
                "id" : new_assignmnet_id,
                "title": title,
                "description" : description,
                    "points" : points,
                    "type" : assignments_type
                }
            )

            with json_path.open("w",encoding="utf-8") as f:
                json.dump(assignments,f)


            st.success("Assignment is recorded!")
            st.dataframe(assignments)