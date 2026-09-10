"""Static configuration: template locations and the fixed coach roster."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
FIELD_TRIP_TEMPLATE = TEMPLATES_DIR / "field_trip_request_template.pdf"
LEAVE_REQUEST_TEMPLATE = TEMPLATES_DIR / "leave_request_template.pdf"

DEFAULT_STUDENT_FORMS_DIR = BASE_DIR / "data" / "student_forms"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"

# The four coaches who can ever appear on a Leave Request Form, with the
# department/supervisor defaults known for each. Blank defaults are filled
# in by hand in the app each trip since they aren't known yet.
COACHES = {
    "Paul Villa": {"department": "Communication Studies", "supervisor": "Janette Funaro"},
    "Robert Hawkins": {"department": "", "supervisor": ""},
    "Tanya Prabhakar": {"department": "", "supervisor": ""},
    "Sydney Alexander": {"department": "", "supervisor": ""},
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
