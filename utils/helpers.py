# helpers.py

import re

# Predefined keyword library for TS Notes matching
KEYWORD_LIBRARY = [
    "battery failure", "ePSA error", "alert", "battery not charging",
    "battery health", "error 2000", "power concern", "battery issue",
    "warning", "hardware replaced"
]

BATTERY_PART_KEYWORDS = [
    "battery", "batt", "battery pack"
]

TAG_MISMATCH_KEYWORDS = ["tag mismatch", "customer mismatch", "serial mismatch"]


def keyword_match_in_notes(ts_notes, keyword_list=KEYWORD_LIBRARY):
    """
    Checks if any keyword in the keyword library is found in the TS Notes.
    """
    ts_notes_lower = ts_notes.lower()
    return any(keyword.lower() in ts_notes_lower for keyword in keyword_list)


def is_battery_part(part_description):
    """
    Checks if the part description refers to a battery.
    """
    part_description_lower = part_description.lower()
    return any(keyword in part_description_lower for keyword in BATTERY_PART_KEYWORDS)


def check_tag_mismatch(ts_notes):
    """
    Detects possible tag mismatch based on TS Notes.
    """
    ts_notes_lower = ts_notes.lower()
    return any(keyword in ts_notes_lower for keyword in TAG_MISMATCH_KEYWORDS)


def normalize_string(text):
    """
    Utility function to normalize and clean strings for comparison.
    """
    return re.sub(r'\s+', ' ', text.strip().lower())


def part_quantity_check(quantity):
    """
    Rule 2: Checks if part quantity is > 1
    """
    try:
        return int(quantity) > 1
    except:
        return False


def is_model_covered(model_description):
    """
    Rule 1: Checks if the model is one of the listed Dell products
    """
    valid_keywords = [
        "product description", "poweredge", "dell storage", "equallogic",
        "dssd product", "power connect"
    ]
    model_description = model_description.lower()
    return any(keyword in model_description for keyword in valid_keywords)
