# Travel Packet Builder

A local Streamlit app that assembles the PDF packet required for every
Forensics (Speech & Debate) tournament trip: fill in the trip details once,
check off who's attending, and it fills the Field Trip Request and Leave
Request forms, builds a roster, and merges everything — in the order your
division office requires — into one downloadable PDF.

Runs entirely on your machine. Nothing is uploaded anywhere, so student data
stays local.

## Packet contents & order

1. **Field Trip Request** — filled from the trip details you enter
2. **Roster** — generated from scratch, listing attending coaches & students
3. **Tournament Invitation** — the PDF you upload (downloaded from the
   tournament's site)
4. **Leave Request Form(s)** — one per attending coach, filled from the
   template
5. **Student Emergency Forms** — the pre-filled PDF for each attending
   student, pulled from your local folder

## Setup

```bash
pip install -r requirements.txt
```

### Student emergency forms

Keep one PDF per student — already filled out — in `data/student_forms/`
(or point the app at wherever you keep them). Name each file after the
student, e.g. `Jane Doe.pdf` or `Doe_Jane.pdf`; the app turns the filename
into the checkbox label you'll pick from when building a packet.

### Coaches

The four coaches who can appear on a Leave Request are fixed in
`packet/config.py` (`COACHES`): Robert Hawkins, Tanya Prabhakar, Sydney
Alexander, and Paul Villa, along with each one's department/supervisor
defaults where known. Edit that file if the roster of coaches ever changes.

## Running it

```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501` — it's still
running locally, nothing leaves your machine.

Then, for each trip:

1. Fill in the trip details (instructor, dates, destination, purpose, etc.)
2. Check off which coaches and students are attending
3. Upload the tournament invitation PDF
4. For each attending coach, review/edit the Leave Request details
   (department, supervisor, reason, and any classes they'll miss)
5. Click **Build packet** and download the merged PDF

## How the forms get filled

- **Leave Request** has real fillable form fields (AcroForm), so it's filled
  directly and correctly regenerates its own appearance.
- **Field Trip Request** has no form fields — it's a flat template — so
  values are overlaid as text at coordinates measured from the blank lines
  on the template PDF itself (see `packet/field_trip_form.py`). If DVC ever
  reissues that template with a different layout, the coordinates in that
  file will need to be re-measured against the new PDF (open it with
  PyMuPDF and call `page.get_text("words")` to find the new blank-line
  positions).

## Project layout

```
app.py                    Streamlit UI
packet/
  config.py                Template paths, coach roster, leave-reason fields
  field_trip_form.py        Fills the Field Trip Request (text overlay)
  leave_request_form.py     Fills a Leave Request (AcroForm)
  roster.py                 Builds the roster PDF from scratch
  students.py                Scans the student emergency form folder
  merge.py                   Merges everything in the required order
templates/                 The blank form templates
data/student_forms/         Your per-student emergency form PDFs (not committed)
output/                     Optional saved copies of built packets (not committed)
```
