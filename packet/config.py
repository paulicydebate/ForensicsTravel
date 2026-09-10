"""Static configuration: template locations and the fixed coach roster."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
FIELD_TRIP_TEMPLATE = TEMPLATES_DIR / "field_trip_request_template.pdf"
LEAVE_REQUEST_TEMPLATE = TEMPLATES_DIR / "leave_request_template.pdf"

DEFAULT_STUDENT_FORMS_DIR = BASE_DIR / "data" / "student_forms"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"

# The four coaches who can ever appear on a Leave Request Form.
COACHES = ["Paul Villa", "Robert Hawkins", "Tanya Prabhakar", "Sydney Alexander"]

# These never change trip to trip, so they're filled in automatically rather
# than asked for in the UI.
LEAVE_REQUEST_SUPERVISOR = "Janette Funaro"
LEAVE_REQUEST_DEPARTMENT = "Communication Studies"

FIELD_TRIP_COURSE = "Comm-163"
FIELD_TRIP_PURPOSE = "Speech and Debate Competition"

# "Section Number" on the Field Trip Request is really a semester choice —
# each semester always reports the same fixed set of section numbers.
SECTION_NUMBER_OPTIONS = {
    "Fall": "2570, 2572, 3243, 4590",
    "Spring": "1524, 1544, 1590, 5413",
}

# Leave-reason checkboxes available on the template, keyed by the AcroForm
# field name, in the order they appear on the form.
LEAVE_REASON_FIELDS = {
    "Sick Leave": "Check Box Sick Leave",
    "Field Trip": "Check Box Fieldtrip",
    "Personal Necessity Leave": "Check Box Personal Necessity Leave",
    "Meeting/Conference": "Check Box Meeting Conference",
    "Vacation Leave": "Check Box Vacation Leave",
    "Jury": "Check Box Jury",
    "Bereavement": "Check Box Bereavement",
    "Other": "Check Box Other",
}
