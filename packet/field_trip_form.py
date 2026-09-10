"""Fills the DVC Field Trip Request template.

The template has no AcroForm fields (it's a flat scanned/printed layout), so
values are overlaid as text at coordinates measured from the blank lines on
the template itself. If DVC ever revises the template's layout, re-measure
these coordinates against the new file (see the "measuring coordinates"
note in the README) before trusting the output.
"""

import pymupdf

from .config import FIELD_TRIP_TEMPLATE

FONT = "helv"
FONT_SIZE = 10

# (x, y) is the text baseline, in the template's own top-left-origin page
# coordinates (same numbers PyMuPDF's get_text("words") reports).
FIELDS = {
    "instructor": (132, 268),
    "today_date": (392, 268),
    "course": (112, 294.9),
    "section_number": (403, 294.9),
    "destination": (132, 348.5),
    "address": (118, 375.4),
    "phone_area": (372, 402.3),
    "phone_number": (402, 402.3),
    "trip_dates": (150, 429.2),
    "time_from": (362, 429.2),
    "time_to": (438, 429.2),
}

DAY_CLASS_CHECKBOX = (75.5, 322)

# The fixed section-number strings are longer than anything hand-written
# would be, so that field gets a smaller font to keep it on the line.
SMALL_FONT_FIELDS = {"section_number"}
SMALL_FONT_SIZE = 8.5

PURPOSE_LINES = [
    # (x, baseline_y, max_width)
    (145.7, 482.8, 534.4 - 145.7),
    (72, 509.8, 465.3),
    (72, 535.3, 465.3),
    (72, 560.7, 465.3),
]


def _wrap_purpose(page, text):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        width = pymupdf.get_text_length(trial, fontname=FONT, fontsize=FONT_SIZE)
        max_width = PURPOSE_LINES[len(lines)][2] if len(lines) < len(PURPOSE_LINES) else PURPOSE_LINES[-1][2]
        if width > max_width and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines[: len(PURPOSE_LINES)]


def fill_field_trip_request(data: dict) -> bytes:
    """data keys: instructor, today_date, course, section_number, destination,
    address, phone_area, phone_number, trip_dates, time_from, time_to, purpose
    """
    doc = pymupdf.open(FIELD_TRIP_TEMPLATE)
    page = doc[0]

    for key, (x, y) in FIELDS.items():
        value = str(data.get(key, "") or "")
        if value:
            fontsize = SMALL_FONT_SIZE if key in SMALL_FONT_FIELDS else FONT_SIZE
            page.insert_text((x, y), value, fontsize=fontsize, fontname=FONT)

    # "Day Class" is always checked per how this form is actually used.
    x, y = DAY_CLASS_CHECKBOX
    page.insert_text((x, y), "X", fontsize=11, fontname=FONT)

    purpose = str(data.get("purpose", "") or "")
    if purpose:
        for line, (x, y, _width) in zip(_wrap_purpose(page, purpose), PURPOSE_LINES):
            page.insert_text((x, y), line, fontsize=FONT_SIZE, fontname=FONT)

    out = doc.tobytes()
    doc.close()
    return out
