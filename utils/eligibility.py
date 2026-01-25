import json

def load_schemes(file_path="data/schemes.json"):
    """
    Loads scheme data from a JSON file.

    Returns:
        List of schemes (list of dictionaries)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_scheme_eligible(scheme, user_profile):
    """
    Checks whether a single scheme is eligible for the given user profile.
    """

    # Age check
    age = user_profile.get("age")
    if age is not None:
        if not (scheme["min_age"] <= age <= scheme["max_age"]):
            return False

    # Education level check
    education = user_profile.get("education")
    if education:
        if scheme["education_level"].lower() != education.lower():
            return False

    # Gender check
    gender = user_profile.get("gender")
    if gender:
        if gender not in scheme["eligible_gender"]:
            return False

    # State check (only for state-level schemes)
    state = user_profile.get("state")
    if scheme["scheme_level"] == "State":
        if state != scheme["state"]:
            return False

    return True


def get_eligible_schemes(user_profile):
    """
    Filters and returns all schemes eligible for the user.
    """

    schemes = load_schemes()
    eligible_schemes = []

    for scheme in schemes:
        if is_scheme_eligible(scheme, user_profile):
            eligible_schemes.append(scheme)

    return eligible_schemes
