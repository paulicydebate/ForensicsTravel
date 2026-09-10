"""Scans a folder of pre-filled Student Emergency Form PDFs and turns each
filename into a display name for the attendance checklist. Name your files
after the student, e.g. "Jane Doe.pdf" or "Doe_Jane.pdf" — underscores and
hyphens are treated as spaces.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class StudentForm:
    display_name: str
    path: Path


def _display_name_from_filename(stem: str) -> str:
    cleaned = stem.replace("_", " ").replace("-", " ")
    cleaned = " ".join(cleaned.split())
    if cleaned == cleaned.lower() or cleaned == cleaned.upper():
        cleaned = cleaned.title()
    return cleaned


def list_student_forms(folder: Path) -> list[StudentForm]:
    folder = Path(folder)
    if not folder.is_dir():
        return []
    forms = [
        StudentForm(display_name=_display_name_from_filename(p.stem), path=p)
        for p in folder.glob("*.pdf")
    ]
    return sorted(forms, key=lambda f: f.display_name.lower())
