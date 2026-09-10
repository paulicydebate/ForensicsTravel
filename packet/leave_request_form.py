"""Fills a Request for Leave form (AcroForm) for one coach."""

import pymupdf

from .config import LEAVE_REQUEST_TEMPLATE

MAX_COURSE_ROWS = 4

TEXT_FIELD_MAP = {
    "first_name": "EMPLOYEE FIRST NAMERow1",
    "last_name": "EMPLOYEE LAST NAME",
    "date_of_request": "DATE OF REQUEST",
    "supervisor": "SUPERVISOR/MANAGER NAME",
    "department": "DEPARTMENT",
    "explanation": "Explanation",
    "dates_for_leave": "DATES FOR LEAVE REQUEST",
    "hours": "HOURS",
    "reason_for_leave": "REASON FOR LEAVE",
}

COURSE_ROW_FIELD_MAP = [
    {
        "course": f"COURSERow{i}",
        "date": f"DATERow{i}",
        "time": f"TIMERow{i}",
        "cancel": f"CANCELRow{i}",
        "sub": f"SUBRow{i}",
        "substitute_name": f"SUBSTITUTE NAMERow{i}",
        "dept_chair_initials": f"DEPT CHAIR INITIALSRow{i}",
    }
    for i in range(1, MAX_COURSE_ROWS + 1)
]


def fill_leave_request(coach_full_name: str, checked_reason_field: str, data: dict, course_rows=None) -> bytes:
    """data keys mirror TEXT_FIELD_MAP minus first_name/last_name (derived from
    coach_full_name). course_rows is a list of up to 4 dicts with keys
    course/date/time/cancel/sub/substitute_name/dept_chair_initials.
    """
    doc = pymupdf.open(LEAVE_REQUEST_TEMPLATE)
    page = doc[0]

    first_name, _, last_name = coach_full_name.partition(" ")
    values = {"first_name": first_name, "last_name": last_name, **data}

    course_rows = course_rows or []

    field_values = {}
    for key, field_name in TEXT_FIELD_MAP.items():
        field_values[field_name] = str(values.get(key, "") or "")

    for row_map, row in zip(COURSE_ROW_FIELD_MAP, course_rows):
        for key, field_name in row_map.items():
            field_values[field_name] = str(row.get(key, "") or "")

    for widget in page.widgets():
        name = widget.field_name
        if name == checked_reason_field:
            widget.field_value = "Yes"
            widget.update()
        elif name in field_values:
            widget.field_value = field_values[name]
            widget.update()

    out = doc.tobytes()
    doc.close()
    return out
