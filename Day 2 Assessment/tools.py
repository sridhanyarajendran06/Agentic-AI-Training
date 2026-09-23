"""Tools for the Student Study Planner assessment."""

SUBJECT_HOURS = {
    "Python": 20,
    "DBMS": 15,
    "Mathematics": 25,
}


def get_subject_hours(subject):
    """Return the available study-material hours for a subject."""
    subject = subject.strip().title()

    if subject not in SUBJECT_HOURS:
        return f"No study-hour data found for {subject}."

    return SUBJECT_HOURS[subject]


def calculator(expression):
    """Evaluate a simple arithmetic expression."""
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except Exception as error:
        return f"Calculation error: {error}"