import streamlit as st
import time
import json
from pathlib import Path
import uuid

#Data layer
def load_data(json_path) -> list:
    if json_path.exists():
        with open(json_path, "r") as f:
            assignments = json.load(f)
    else:
        assignments = []

    return assignments

def save_data(assignments: list, json_path) -> None:
    with open(json_path, "w") as f:
        json.dump(assignments,f)
    
# Service Layer
def add_new_assignment(assignments: list) -> list:
    assignments.append(
                {
                    "id" : str(uuid.uuid4()),
                    "title": st.session_state['draft']['title'],
                    'description' : st.session_state['draft']['description'],
                    'points': st.session_state['draft']['points'],
                    'type': st.session_state['draft']['type']
                }
            )
    
    return assignments

def edit_assignment(assignments: list) -> list:
    for assignment in assignments:
        if assignment["id"] == st.session_state["draft"]['id']:
            assignment['title'] = st.session_state['draft']['title']
            assignment['description'] = st.session_state['draft']['description']
            assignment['points'] =  st.session_state['draft']['points']
            assignment['type'] = st.session_state['draft']['type']
            break
    return assignments
                                                              
#UI Layer
def render_dashboard(assignments):
    col1,col2 = st.columns([3,1])

    with col1:
        st.subheader("Assignments")
    
    with col2: 
        if st.button("Add New Assignment",key="add_new_assignment_btn",
                     type="primary",use_container_width=True):
            st.session_state["page"] = "Add New Assignment"
            st.rerun()

    with st.container(border= True):
        for assignment in assignments:
            with st.container(border=True):
                st.markdown(f"Title: {assignment['title']}")
                st.markdown(f"Description: {assignment['description']}")
                if st.button("Edit", key = f"edit_btn_{assignment['id']}", type="primary",use_container_width=True):
                    st.session_state["draft"] = assignment
                    st.session_state["page"] = "Edit Assignment"
                    st.rerun()
            st.divider()


def render_add_edit_new_assignment(assignments, json_path):
    col1,col2 = st.columns([3,1])

    with col1:
        st.subheader("Add New Assignment")
    with col2:
        if st.button("Back", key="back_btn", type="secondary"):
            st.session_state["page"] = "Assignment Dashboard"
            st.rerun()

    st.session_state['draft']['title'] = st.text_input("Title" , key="title_txt_input", value=st.session_state['draft'].get('title', ''))
    st.session_state['draft']['description'] = st.text_area("Description", key="description_txt_input",
                                                            value= st.session_state['draft'].get('description', ''),
                                                             placeholder="normalization is covered here",
                            help="Here you are entering the assignment details")
    st.session_state["draft"]['points'] = st.number_input("Points", key="points_input",
                                                          value = st.session_state['draft'].get('points', 0))
    
    options = ["Select an option", "Homework", "Lab", "other"]
    draft_assignment_type = st.session_state['draft'].get('type')
    if draft_assignment_type in options:
        draft_assignment_type_index = options.index(draft_assignment_type)
    else: 
        draft_assignment_type_index = 0

    st.session_state['draft']['type'] = st.selectbox("Type", 
                                                                options,
                                                                key="type_selector",
                                                                index=draft_assignment_type_index)
    
    if st.button("Save", key="save_btn", type="primary",use_container_width=True):
        with st.spinner("In progress..."):
            time.sleep(3)

            #Add new assignment to the assignments
            # service Layer
            if st.session_state["page"] == "Add New Assignment":
                assignments = add_new_assignment(assignments)
            elif st.session_state["page"] == "Edit Assignment":
                assignments = edit_assignment(assignments)


            #Data Layer
            save_data(assignments, json_path=json_path)

            st.success("Assignment is recorded.")
            time.sleep(3)
            st.session_state["draft"] = {}
            st.session_state['page'] = "Assignment Dashboard"
            st.rerun()


def main():
    st.set_page_config(page_title="Course Management",
                   layout="centered",
                   initial_sidebar_state="collapsed")

    st.title("Course Management")
    st.divider()

    #0.2 Loading the Data
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

    #3 Session State Initialization
    if "page" not in st.session_state:
        st.session_state['page'] = "Assignment Dashboard"

    if "draft" not in st.session_state:
        st.session_state['draft'] = {}

    if st.session_state["page"] == "Assignment Dashboard":
        render_dashboard(assignments=assignments)
    elif st.session_state["page"] == "Add New Assignment":
        render_add_edit_new_assignment(assignments=assignments, json_path=json_path)
    elif st.session_state["page"] == "Edit Assignment":
        render_add_edit_new_assignment(assignments=assignments,json_path=json_path)
    

if __name__ == "__main__":
    main()