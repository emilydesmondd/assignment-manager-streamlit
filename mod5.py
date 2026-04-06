import streamlit as st
import time
import json
from pathlib import Path
import uuid

st.set_page_config(
    page_title="Course Management",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Course Management App")
st.divider()


# Placeholder Default Data
assignments = [
    {
        "id": "HW1",
        "title": "Intro to Database",
        "description": "basics of database design",
        "points": 100,
        "type": "homework"
    },
    {
        "id": "HW2",
        "title": "Normalization",
        "description": "normalizing",
        "points": 100,
        "type": "homework"
    }
]

json_path = Path("assignments.json")

# Load the data from a json file if it exists
if json_path.exists():
    with open(json_path, "r", encoding="utf-8") as f:
        assignments = json.load(f)


if "page" not in st.session_state:
    st.session_state["page"] = "Assignments Dashboard"

if "draft" not in st.session_state:
    st.session_state["draft"] = {}

if st.session_state["page"] == "Assignments Dashboard":
    st.subheader("Assignments")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Assignments Dashboard")
    with col2:
        if st.button("Add New Assignment", key="add_btn", use_container_width=False):
            st.session_state["page"] = "Add Assignment"
            st.rerun()


elif st.session_state["page"] == "Add Assignment":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Add New Assignment")
    with col2:
        if st.button("Back", key="back_btn", use_container_width=False):
            st.session_state["page"] = "Assignments Dashboard" 
            st.rerun()

    st.session_state['draft']['title'] = st.text_input("Title")
    st.session_state['draft']['description'] = st.text_area("Description", placeholder="normalization is covered here",
                            help="Here you are entering the assignment details")
    st.session_state["draft"]['points'] = st.number_input("Points")

    st.session_state['draft']['assignment_type'] = st.selectbox("Type", ["Select an option", "Homework", "Lab", "other"])
    if st.session_state["draft"]['assignment_type'] == "other":
        st.session_state["draft"]['assignment_type'] = st.text_input("Type", placeholder="Enter the assignment Type")

    # Live Preview
    with st.container(border=True):
        with st.expander("Assignment Details", expanded=True):
            # Using .get() for safe dictionary access on initial load
            st.markdown(f"### Title: {st.session_state['draft'].get('title', '')}")
            st.markdown(f"**Description**: {st.session_state['draft'].get('description', '')}")
            st.markdown(f"Type: **{st.session_state['draft'].get('assignment_type', '')}**")
    
    # Save Action
    btn_save = st.button("Save", use_container_width=True, key="save_btn", type="primary")

    if btn_save:
        if not st.session_state['draft'].get('title'):
            st.warning("Title needs to be provided!")
        else:
            with st.spinner("Assignment is being recorded...."):
                time.sleep(2)
                
                # Append to list
                assignments.append(
                    {
                        "id": str(uuid.uuid4()),
                        "title": st.session_state['draft']['title'],
                        "description": st.session_state['draft']['description'],
                        "points": st.session_state['draft']['points'],
                        "type": st.session_state['draft']['assignment_type']
                    }
                )

                # Record directly into JSON file 
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(assignments, f, indent=4)

                st.success("New Assignment is recorded!")
                st.info("This is a new assignment")
                
                time.sleep(2)
                st.session_state["page"] = "Assignments Dashboard"
                st.session_state["draft"] = {}
                st.rerun()

else:
    st.session_state["page"] = "Edit Assignment"
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Edit Assignment")
    with col2:
        if st.button("Back", key="back_btn_edit", use_container_width=False):
            st.session_state["page"] = "Assignments Dashboard" 
            st.rerun()
