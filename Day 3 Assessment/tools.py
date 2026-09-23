"""Single external tool for the Day 3 assessment."""

SUBJECT_HOURS = {
    "Python": 20,
    "DBMS": 15,
    "Mathematics": 25,
}


def get_subject_hours(subject):
    """Look up the available study-material hours for a subject."""
    subject = subject.strip().lower()

    subjects = {
        "python": 20,
        "dbms": 15,
        "mathematics": 25,
    }

    if subject not in subjects:
        return f"No study-hour data found for {subject}."

    return str(subjects[subject])