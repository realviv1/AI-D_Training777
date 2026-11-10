import re


MAX_LENGTH = 500


ALLOWED_KEYWORDS = [
    "restaurant",
    "food",
    "cuisine",
    "dining",
    "cost",
    "guest",
    "table",
    "indian",
    "italian",
    "chinese",
    "north indian",
    "south indian",
    "restaurant id",
    "people",
    "seat",
    "reservation"
]


FOLLOW_UPS = [
    "yes",
    "no",
    "ok",
    "okay",
    "4 people",
    "5 people",
    "6 people",
    "7 people",
    "8 people"
]


def detect_pii(text):

    email_pattern = r'\S+@\S+\.\S+'
    phone_pattern = r'\b\d{10}\b'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    return emails, phones


def redact_pii(text):

    text = re.sub(
        r'\S+@\S+\.\S+',
        '[REDACTED_EMAIL]',
        text
    )

    text = re.sub(
        r'\b\d{10}\b',
        '[REDACTED_PHONE]',
        text
    )

    return text


def validate_user_input(text):

    text = text.strip()

    if not text:
        return False, "Question cannot be empty."

    if len(text) > MAX_LENGTH:
        return False, "Question too long."

    lowered = text.lower()

    if lowered in FOLLOW_UPS:
        return True, None

    if any(
        keyword in lowered
        for keyword in ALLOWED_KEYWORDS
    ):
        return True, None

    return (
        False,
        "Only restaurant related questions are allowed."
    )