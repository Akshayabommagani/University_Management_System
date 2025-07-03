# University Management System

import streamlit as st
import pickle
import os
from models import person, student, teacher, college

# --- Add University Background Image ---
st.markdown("""
    <style>
    body, .stApp {
        background-image: url('https://images.unsplash.com/photo-1503676382389-4809596d5290?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp {
        background-color: rgba(247,250,253,0.92) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add back the main title at the top of the app
st.markdown("""
    <h1 style='color:#fff; font-size: 2.8rem; font-weight: 900; letter-spacing:1px; text-align:center; margin-bottom: 0.5em;'>University Management System</h1>
""", unsafe_allow_html=True)

# Creating the Menu Bar
menu_choice = st.sidebar.radio(
    "Select Action",
    (
        "Create College",
        "Add Student",
        "Add Teacher",
        "Display students",
        "Display Teachers",
        "Display Colleges"
    )
)

if "colleges" not in st.session_state:
    st.session_state.colleges = []

def find_college(cname):
    return next((c for c in st.session_state.colleges if c.cname == cname), None)

# Add Save/Load buttons to sidebar
save_colleges = st.sidebar.button("💾 Save Data", key="save_data_btn")
load_colleges = st.sidebar.button("📂 Load Data", key="load_data_btn")
DATA_FILE = "colleges_data.pkl"

if save_colleges:
    try:
        with open(DATA_FILE, "wb") as f:
            pickle.dump(st.session_state.colleges, f)
        st.sidebar.success("Data saved successfully!")
    except Exception as e:
        st.sidebar.error(f"Error saving data: {e}")

if load_colleges:
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f:
                st.session_state.colleges = pickle.load(f)
            st.sidebar.success("Data loaded successfully!")
            st.experimental_rerun()
        else:
            st.sidebar.error("No saved data found.")
    except Exception as e:
        st.sidebar.error(f"Error loading data: {e}")

# --- Edit/Delete Student and Teacher ---
def delete_student(college_obj, idx):
    del college_obj.students[idx]

def delete_teacher(college_obj, idx):
    del college_obj.teachers[idx]

# --- Add/Edit/Delete in UI ---

# Created new college
if menu_choice == "Create College":
    cname = st.text_input("Enter new college name")
    if st.button("Create"):
        if not cname:
            st.error("College name is empty, plz write some college name")
        elif find_college(cname):
            st.warning("This college already exist")
        else:
            st.session_state.colleges.append(college(cname))
            st.success(f"Created College successfully: {cname}")

elif menu_choice == "Add Student":
    st.markdown("<h3 style='color:#fff; font-weight:700;'>Add Student</h3>", unsafe_allow_html=True)
    if not st.session_state.colleges:
        st.info("Please Create college first")
    else:
        clgname = st.selectbox("Choose College", [c.cname for c in st.session_state.colleges], key="add_student_clg")
        st.text(f"Selected College: {clgname}")
        roll = st.text_input("Roll Number")
        sname = st.text_input("Student Name")
        branch = st.text_input("Branch e.g. CSE")
        if st.button("Add Student"):
            if not(roll and sname and branch):
                st.error("All fields are mandatory")
            else:
                clg = find_college(clgname)
                clg.add_student(student(roll, sname, branch))
                st.success("Student added successfully")

elif menu_choice == "Add Teacher":
    st.markdown("<h3 style='color:#fff; font-weight:700;'>Add Teacher</h3>", unsafe_allow_html=True)
    if not st.session_state.colleges:
        st.info("Please Create college first")
    else:
        clgname = st.selectbox("Choose College", [c.cname for c in st.session_state.colleges], key="add_teacher_clg")
        st.text(f"Selected College: {clgname}")
        subj = st.text_input("Subject")
        tname = st.text_input("Teacher Name")
        branch = st.text_input("Branch e.g. CSE")
        if st.button("Add Teacher"):
            if not(subj and tname and branch):
                st.error("All fields are mandatory")
            else:
                clg = find_college(clgname)
                clg.add_teacher(teacher(branch, tname, subj))
                st.success("Teacher added successfully")

elif menu_choice == "Display students":
    if not st.session_state.colleges:
        st.info("Please Create college first")
    else:
        clgname = st.selectbox("Choose College", [c.cname for c in st.session_state.colleges], key="display_students_clg")
        st.subheader(f"List of Students from {clgname}")
        clg = find_college(clgname)
        if clg.students:
            for i, s in enumerate(clg.students, 1):
                col1, col2 = st.columns([7, 3])
                with col1:
                    st.markdown(f"<span class='student-teacher-name'>{i} : {s}</span>", unsafe_allow_html=True)
                with col2:
                    edit = st.button(f"Edit", key=f"edit_student_{clgname}_{i}")
                    delete = st.button(f"Delete", key=f"delete_student_{clgname}_{i}")
                    if edit:
                        new_name = st.text_input(f"Edit Name for Roll {s.rollno}", value=s.name, key=f"edit_name_{clgname}_{i}")
                        new_branch = st.text_input(f"Edit Branch for Roll {s.rollno}", value=s.branch, key=f"edit_branch_{clgname}_{i}")
                        save_col1, save_col2 = st.columns([1,1])
                        with save_col1:
                            save = st.button(f"Save", key=f"save_student_{clgname}_{i}")
                        with save_col2:
                            cancel = st.button(f"Cancel", key=f"cancel_student_{clgname}_{i}")
                        if save:
                            s.name = new_name
                            s.branch = new_branch
                            st.success("Student updated!")
                        # Cancel just closes the edit UI (handled by rerun)
                    if delete:
                        delete_student(clg, i-1)
                        st.success("Student deleted!")
                        st.experimental_rerun()
        else:
            st.warning("No Student admitted in this college")

elif menu_choice == "Display Teachers":
    if not st.session_state.colleges:
        st.info("Please Create college first")
    else:
        clgname = st.selectbox("Choose College", [c.cname for c in st.session_state.colleges], key="display_teachers_clg")
        st.subheader(f"List of Teachers from {clgname}")
        clg = find_college(clgname)
        if clg.teachers:
            for i, t in enumerate(clg.teachers, 1):
                col1, col2 = st.columns([7, 3])
                with col1:
                    st.markdown(f"<span class='student-teacher-name'>{i} : {t}</span>", unsafe_allow_html=True)
                with col2:
                    edit = st.button(f"Edit", key=f"edit_teacher_{clgname}_{i}")
                    delete = st.button(f"Delete", key=f"delete_teacher_{clgname}_{i}")
                    if edit:
                        new_name = st.text_input(f"Edit Name for Teacher {t.name}", value=t.name, key=f"edit_tname_{clgname}_{i}")
                        new_branch = st.text_input(f"Edit Branch for Teacher {t.name}", value=t.branch, key=f"edit_tbranch_{clgname}_{i}")
                        new_subject = st.text_input(f"Edit Subject for Teacher {t.name}", value=t.subject, key=f"edit_tsubj_{clgname}_{i}")
                        save_col1, save_col2 = st.columns([1,1])
                        with save_col1:
                            save = st.button(f"Save", key=f"save_teacher_{clgname}_{i}")
                        with save_col2:
                            cancel = st.button(f"Cancel", key=f"cancel_teacher_{clgname}_{i}")
                        if save:
                            t.name = new_name
                            t.branch = new_branch
                            t.subject = new_subject
                            st.success("Teacher updated!")
                        # Cancel just closes the edit UI (handled by rerun)
                    if delete:
                        delete_teacher(clg, i-1)
                        st.success("Teacher deleted!")
                        st.experimental_rerun()
        else:
            st.warning("No Teacher in this college")

elif menu_choice == "Display Colleges":
    st.subheader("All colleges list")
    if not st.session_state.colleges:
        st.info("No college added")
    else:
        for i, c in enumerate(st.session_state.colleges, 1):
            st.markdown(f"<span class='student-teacher-name'>{i} : {c.cname}</span>", unsafe_allow_html=True)

# --- Modern University Management System UI ---
# Apply a dark theme: black background, all fonts white, white headings, white input text, and dark cards
st.markdown("""
    <style>
    html, body, [class*='css']  {
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        background: #111 !important;
        color: #fff !important;
    }
    .stApp {
        background: #111 !important;
        color: #fff !important;
    }
    * {
        color: #fff !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #222 0%, #333 100%);
        color: #fff !important;
        border-radius: 12px;
        font-size: 20px;
        padding: 14px 36px;
        margin: 10px 0px;
        border: none;
        font-weight: 700;
        box-shadow: 0 2px 8px #0008;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #333 0%, #222 100%);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px;
        border: none;
        padding: 14px 20px;
        font-size: 20px;
        color: #fff !important;
        background: #222 !important;
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        font-weight: 600;
        box-shadow: 0 2px 8px #0008;
    }
    ::placeholder {
        color: #bbb !important;
        opacity: 1;
        font-size: 20px;
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
    }
    .stSidebarContent {
        background: linear-gradient(120deg, #222 0%, #333 100%) !important;
        padding: 24px 12px 24px 12px !important;
        color: #fff !important;
    }
    .sidebar-title {
        color: #fff !important;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sidebar-desc {
        color: #fff !important;
        font-size: 16px;
        margin-bottom: 12px;
    }
    .st-cb, .st-cg, .st-ch, .st-ci {
        background: #222;
        border-radius: 16px;
        box-shadow: 0 4px 16px #0008;
        padding: 28px 36px;
        margin-bottom: 28px;
        color: #fff !important;
    }
    h1, h2, h3, h4, h5, .stInfo, .stWarning, .stSuccess, .stError {
        color: #fff !important;
        font-weight: 900;
        letter-spacing: 1px;
    }
    .stInfo, .stWarning, .stSuccess, .stError {
        background: #222 !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }
    .student-teacher-name {
        font-size: 22px;
        color: #fff !important;
        font-weight: 700;
        background: #222;
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: block;
    }
    .ums-card {
        background: #222;
        border-radius: 18px;
        box-shadow: 0 6px 24px #0008;
        padding: 36px 40px 30px 40px;
        margin: 30px auto 30px auto;
        max-width: 900px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style='text-align:center;'>
        <img src='https://img.icons8.com/ios-filled/100/ffffff/university.png' width='80'/>
        <div class='sidebar-title'>UMS Portal</div>
        <div class='sidebar-desc'>A modern, official University Management System.<br>Manage colleges, students, and teachers with ease.</div>
    </div>
    <hr style='border:1px solid #fff;'>
""", unsafe_allow_html=True)