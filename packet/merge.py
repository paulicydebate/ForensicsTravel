"""Merges the individual pieces into one packet, in the required order:
Field Trip Request, Roster, Tournament Invite, Leave Request Form(s),
Student Emergency Forms.
"""

from pathlib import Path

import pymupdf


def _append(target: "pymupdf.Document", source):
    """source is PDF bytes, or a filesystem path."""
    if isinstance(source, (bytes, bytearray)):
        doc = pymupdf.open(stream=bytes(source), filetype="pdf")
    else:
        doc = pymupdf.open(str(source))
    target.insert_pdf(doc)
    doc.close()


def build_packet(field_trip_request_bytes: bytes, roster_bytes: bytes,
                  tournament_invite_bytes: bytes | None,
                  leave_request_bytes_list: list[bytes],
                  student_form_paths: list[Path]) -> bytes:
    target = pymupdf.open()

    _append(target, field_trip_request_bytes)
    _append(target, roster_bytes)

    if tournament_invite_bytes:
        _append(target, tournament_invite_bytes)

    for leave_bytes in leave_request_bytes_list:
        _append(target, leave_bytes)

    for path in student_form_paths:
        _append(target, path)

    out = target.tobytes()
    target.close()
    return out
