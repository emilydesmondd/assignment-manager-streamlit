import streamlit as st
import json
from pathlib import Path
from datetime import datetime

json_file = Path("requests.json")

requests = [
    {
        "status": "Pending",
        "course_id": "011101",
        "student_email": "jsmith@university.edu",
        "absence_date": "2026-03-25",
        "submitted_timestamp": "2026-03-19 08:30:00",
        "excuse_type": "Medical",
        "explanation": "I have a scheduled doctor's appointment that I cannot reschedule.",
        "instructor_note": ""
    }
]

json_file = Path("requests.json")

if json_file.exists() and json_file.stat().st_size > 0:
    with open(json_file, "r") as f:
        requests = json.load(f)
else:
    requests = []  
    with open(json_file, "w") as f:
        json.dump(requests, f, indent=4)


if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

if "selected_request" not in st.session_state:
    st.session_state["selected_request"] = None


st.sidebar.title("Navigation")

if st.sidebar.button("Dashboard", key="nav_dashboard"):
    st.session_state["page"] = "Dashboard"
    st.rerun()

if st.sidebar.button("Request Form", key="nav_request_form"):
    st.session_state["page"] = "Request Form"
    st.rerun()


if st.session_state["page"] == "Dashboard":
    st.title("Excused Absence Dashboard")

    if len(requests) == 0:
        st.write("No requests found.")
    else:
        event = st.dataframe(
            requests,
            on_select="rerun",
            selection_mode="single-row",
            key="dashboard_requests_df"
        )

        if event.selection.rows:
            selected_index = event.selection.rows[0]
            st.session_state["selected_request"] = requests[selected_index]

        if st.session_state["selected_request"] is not None:
            selected = st.session_state["selected_request"]

            st.subheader("Selected Request Details")
            st.write("**Status:**", selected["status"])
            st.write("**Course ID:**", selected["course_id"])
            st.write("**Student Email:**", selected["student_email"])
            st.write("**Absence Date:**", selected["absence_date"])
            st.write("**Submitted Timestamp:**", selected["submitted_timestamp"])
            st.write("**Excuse Type:**", selected["excuse_type"])
            st.write("**Explanation:**", selected["explanation"])
            st.write("**Instructor Note:**", selected["instructor_note"])


elif st.session_state["page"] == "Request":
    st.title("Excused Absence Request Form")
    st.write("This page is being developed.")
