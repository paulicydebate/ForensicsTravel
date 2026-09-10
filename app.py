import datetime as dt
from pathlib import Path

import pandas as pd
import streamlit as st

from packet.config import COACHES, DEFAULT_STUDENT_FORMS_DIR, DEFAULT_OUTPUT_DIR, LEAVE_REASON_FIELDS
from packet.field_trip_form import fill_field_trip_request
from packet.leave_request_form import fill_leave_request
from packet.roster import build_roster_pdf
from packet.students import list_student_forms
from packet.merge import build_packet

st.set_page_config(page_title="Travel Packet Builder", layout="wide")
st.title("Travel Packet Builder")
st.caption(
    "Fills the Field Trip Request and Leave Request forms, builds a roster, "
    "and merges everything with the tournament invite and student emergency "
    "forms into one packet — in the order your office requires it."
)

COURSE_ROW_COLUMNS = ["Course", "Date", "Time", "Cancel?", "Sub?", "Substitute Name", "Dept Chair Initials"]
EMPTY_COURSE_ROWS = pd.DataFrame([["", "", "", "", "", "", ""]] * 4, columns=COURSE_ROW_COLUMNS)

# ---------------------------------------------------------------- Trip info

st.header("1. Trip details")
col1, col2 = st.columns(2)
with col1:
    tournament_name = st.text_input("Tournament / event name", placeholder="e.g. Golden Gate Invitational")
    instructor = st.text_input("Instructor name(s)", value="Paul Villa")
    today_date = st.date_input("Today's date", value=dt.date.today())
    course = st.text_input("Course")
    section_number = st.text_input("Section number")
with col2:
    destination = st.text_input("Destination")
    address = st.text_input("Address")
    phone_col1, phone_col2 = st.columns([1, 3])
    phone_area = phone_col1.text_input("Area code", max_chars=3)
    phone_number = phone_col2.text_input("Phone number")

col3, col4, col5 = st.columns(3)
trip_dates = col3.text_input("Date(s) of trip", placeholder="e.g. 3/12 - 3/15")
time_from = col4.text_input("Time from (depart)", placeholder="e.g. 9:35am")
time_to = col5.text_input("Time to (return)", placeholder="e.g. 5:00pm")

purpose = st.text_area("Purpose of trip", height=80,
                        placeholder="e.g. Traveling to compete at the Golden Gate Invitational speech tournament.")

trip_data = {
    "instructor": instructor,
    "today_date": today_date.strftime("%m/%d/%Y") if today_date else "",
    "course": course,
    "section_number": section_number,
    "destination": destination,
    "address": address,
    "phone_area": phone_area,
    "phone_number": phone_number,
    "trip_dates": trip_dates,
    "time_from": time_from,
    "time_to": time_to,
    "purpose": purpose,
}

# ---------------------------------------------------------------- Attendees

st.header("2. Who's attending")

col_coaches, col_students = st.columns(2)

with col_coaches:
    st.subheader("Coaches (Leave Request needed)")
    selected_coaches = []
    for name in COACHES:
        if st.checkbox(name, key=f"coach_{name}"):
            selected_coaches.append(name)

with col_students:
    st.subheader("Students")
    student_dir_input = st.text_input("Student emergency forms folder", value=str(DEFAULT_STUDENT_FORMS_DIR))
    student_forms = list_student_forms(Path(student_dir_input))

    if not student_forms:
        st.info(f"No PDFs found in {student_dir_input}. Add each student's pre-filled "
                f"emergency form there, named after the student (e.g. \"Jane Doe.pdf\").")
        selected_students = []
    else:
        select_all = st.checkbox("Select all", key="students_select_all")
        selected_students = []
        for form in student_forms:
            checked = st.checkbox(form.display_name, value=select_all, key=f"student_{form.path.name}")
            if checked:
                selected_students.append(form)

# ---------------------------------------------------------------- Tournament invite

st.header("3. Tournament invitation")
invite_file = st.file_uploader("Tournament invitation PDF", type=["pdf"])

# ---------------------------------------------------------------- Leave requests

leave_request_inputs = {}
if selected_coaches:
    st.header("4. Leave Request details")
    for coach in selected_coaches:
        defaults = COACHES[coach]
        with st.expander(f"Leave Request — {coach}", expanded=True):
            lc1, lc2 = st.columns(2)
            department = lc1.text_input("Department", value=defaults["department"], key=f"dept_{coach}")
            supervisor = lc2.text_input("Supervisor/Manager", value=defaults["supervisor"], key=f"sup_{coach}")

            reason_label = st.selectbox("Reason for leave (checkbox on form)", list(LEAVE_REASON_FIELDS.keys()),
                                         index=list(LEAVE_REASON_FIELDS.keys()).index("Meeting/Conference"),
                                         key=f"reason_{coach}")

            explanation = st.text_input("Explanation", value=tournament_name, key=f"expl_{coach}")
            dates_for_leave = st.text_input("Dates for leave request", value=trip_dates, key=f"dates_{coach}")
            default_reason_text = (
                f"Taking students to {tournament_name} in {destination}"
                if tournament_name or destination else ""
            )
            reason_for_leave = st.text_area("Reason for leave", value=default_reason_text, height=60,
                                             key=f"reasontext_{coach}")

            st.caption("Classes missed while away (leave rows blank if not needed):")
            course_rows_df = st.data_editor(EMPTY_COURSE_ROWS, num_rows="fixed", hide_index=True,
                                             key=f"courses_{coach}")

            leave_request_inputs[coach] = {
                "department": department,
                "supervisor": supervisor,
                "reason_field": LEAVE_REASON_FIELDS[reason_label],
                "explanation": explanation,
                "dates_for_leave": dates_for_leave,
                "reason_for_leave": reason_for_leave,
                "course_rows": [
                    {
                        "course": row["Course"],
                        "date": row["Date"],
                        "time": row["Time"],
                        "cancel": row["Cancel?"],
                        "sub": row["Sub?"],
                        "substitute_name": row["Substitute Name"],
                        "dept_chair_initials": row["Dept Chair Initials"],
                    }
                    for _, row in course_rows_df.iterrows()
                    if any(str(v).strip() for v in row)
                ],
            }

# ---------------------------------------------------------------- Generate

st.header("5. Generate packet")

missing = []
if not instructor:
    missing.append("Instructor name")
if not destination:
    missing.append("Destination")
if not trip_dates:
    missing.append("Date(s) of trip")
if not selected_students:
    missing.append("At least one student")

if missing:
    st.warning("Still needed: " + ", ".join(missing))

if st.button("Build packet", type="primary", disabled=bool(missing)):
    with st.spinner("Filling forms and merging packet..."):
        field_trip_bytes = fill_field_trip_request(trip_data)

        roster_bytes = build_roster_pdf(
            tournament_name=tournament_name,
            destination=destination,
            trip_dates=trip_dates,
            coaches=selected_coaches,
            students=[f.display_name for f in selected_students],
        )

        invite_bytes = invite_file.read() if invite_file is not None else None

        leave_bytes_list = []
        for coach in selected_coaches:
            inputs = leave_request_inputs[coach]
            leave_bytes_list.append(fill_leave_request(
                coach_full_name=coach,
                checked_reason_field=inputs["reason_field"],
                data={
                    "date_of_request": trip_data["today_date"],
                    "supervisor": inputs["supervisor"],
                    "department": inputs["department"],
                    "explanation": inputs["explanation"],
                    "dates_for_leave": inputs["dates_for_leave"],
                    "reason_for_leave": inputs["reason_for_leave"],
                },
                course_rows=inputs["course_rows"],
            ))

        student_paths = [f.path for f in selected_students]

        packet_bytes = build_packet(
            field_trip_request_bytes=field_trip_bytes,
            roster_bytes=roster_bytes,
            tournament_invite_bytes=invite_bytes,
            leave_request_bytes_list=leave_bytes_list,
            student_form_paths=student_paths,
        )

    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in (tournament_name or "trip")).strip() or "trip"
    filename = f"{safe_name.replace(' ', '_')}_packet.pdf"

    st.session_state["packet_bytes"] = packet_bytes
    st.session_state["packet_filename"] = filename
    st.success("Packet built.")

if st.session_state.get("packet_bytes"):
    st.download_button("Download packet", data=st.session_state["packet_bytes"],
                        file_name=st.session_state["packet_filename"], mime="application/pdf")

    if st.checkbox("Also save a copy to the output/ folder"):
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DEFAULT_OUTPUT_DIR / st.session_state["packet_filename"]
        out_path.write_bytes(st.session_state["packet_bytes"])
        st.info(f"Saved to {out_path}")
