"""Builds the roster PDF (coaches + attending students) from scratch."""

import pymupdf

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
MARGIN = 72


def _draw_name_list(page, y, title, names):
    page.insert_text((MARGIN, y), title, fontsize=13, fontname="hebo")
    y += 20
    if not names:
        page.insert_text((MARGIN + 20, y), "(none)", fontsize=11, fontname="heit")
        y += 18
        return y
    for name in names:
        box = pymupdf.Rect(MARGIN, y - 10, MARGIN + 12, y + 2)
        page.draw_rect(box, color=(0, 0, 0), width=0.8)
        page.insert_text((MARGIN + 2, y), "X", fontsize=10, fontname="hebo")
        page.insert_text((MARGIN + 22, y), name, fontsize=11, fontname="helv")
        y += 18
    return y


def build_roster_pdf(tournament_name: str, destination: str, trip_dates: str,
                      coaches: list[str], students: list[str]) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

    y = MARGIN
    page.insert_text((MARGIN, y), "Travel Roster", fontsize=18, fontname="hebo")
    y += 26
    if tournament_name:
        page.insert_text((MARGIN, y), tournament_name, fontsize=12, fontname="helv")
        y += 16
    if destination:
        page.insert_text((MARGIN, y), f"Destination: {destination}", fontsize=11, fontname="helv")
        y += 16
    if trip_dates:
        page.insert_text((MARGIN, y), f"Date(s): {trip_dates}", fontsize=11, fontname="helv")
        y += 16

    y += 16
    y = _draw_name_list(page, y, f"Coaches ({len(coaches)})", coaches)
    y += 20
    y = _draw_name_list(page, y, f"Students ({len(students)})", students)

    out = doc.tobytes()
    doc.close()
    return out
