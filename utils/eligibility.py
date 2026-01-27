import json

# --------------------------------------------------
# Utility: normalize text for safe comparison
# --------------------------------------------------
def normalize(text):
    if not text:
        return ""
    return text.strip().lower()


# --------------------------------------------------
# Load schemes from JSON
# --------------------------------------------------
def load_schemes(file_path="data/schemes.json"):
    """
    Loads scheme data from a JSON file.

    Returns:
        List of schemes (list of dictionaries)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# Education normalization map
# --------------------------------------------------
EDUCATION_MAP = {
    "No Formal Education": ["any"],
    "School": ["school", "any"],
    "Higher Secondary": ["higher secondary", "any"],
    "Diploma": ["diploma", "any"],
    "Undergraduate": ["undergraduate", "graduate", "any"],
    "Postgraduate": ["postgraduate", "any"],
    "Research": ["postgraduate", "any"],
    "Skill Training": ["skill training", "any"],
    "Any": ["any"]
}


# --------------------------------------------------
# Single scheme eligibility check
# --------------------------------------------------
def is_scheme_eligible(scheme, user_profile):
    """
    Checks whether a single scheme is eligible for the given user profile.
    """

    # ------------------------------
    # Age check
    # ------------------------------
    age = user_profile.get("age")
    if age is not None:
        min_age = scheme.get("min_age", 0)
        max_age = scheme.get("max_age", 100)
        if not (min_age <= age <= max_age):
            return False

    # ------------------------------
    # Education level check
    # ------------------------------
    user_education = user_profile.get("education", "Any")
    scheme_education = scheme.get("education_level", "Any")

    allowed_levels = EDUCATION_MAP.get(
        user_education, ["any"]
    )

    if normalize(scheme_education) not in allowed_levels and normalize(scheme_education) != "any":
        return False

    # ------------------------------
    # Gender check
    # ------------------------------
    gender = user_profile.get("gender")
    if gender:
        eligible_genders = [normalize(g) for g in scheme.get("eligible_gender", [])]
        if normalize(gender) not in eligible_genders:
            return False

    # ------------------------------
    # Occupation check
    # ------------------------------
    occupation = user_profile.get("occupation", "Citizen")
    scheme_occupations = scheme.get("eligible_occupation", ["All"])

    scheme_occupations = [normalize(o) for o in scheme_occupations]

    if "all" not in scheme_occupations:
        if normalize(occupation) not in scheme_occupations:
            return False

    # ------------------------------
    # State vs Central scheme check
    # ------------------------------
    scheme_level = normalize(scheme.get("scheme_level"))
    scheme_state = normalize(scheme.get("state"))
    user_state = normalize(user_profile.get("state"))

    if scheme_level == "state":
        if scheme_state != user_state:
            return False
    # Central schemes valid for all states (including "All")

    return True


# --------------------------------------------------
# Main eligibility function
# --------------------------------------------------
def get_eligible_schemes(user_profile):
    """
    Filters and returns all schemes eligible for the user.
    Includes a safe fallback to avoid empty results.
    """

    schemes = load_schemes()
    eligible_schemes = []

    for scheme in schemes:
        if is_scheme_eligible(scheme, user_profile):
            eligible_schemes.append(scheme)

    # --------------------------------------------------
    # Safe fallback (UX-friendly, not misleading)
    # --------------------------------------------------
    if not eligible_schemes:
        user_state = normalize(user_profile.get("state"))

        for scheme in schemes:
            scheme_level = normalize(scheme.get("scheme_level"))
            scheme_state = normalize(scheme.get("state"))

            if scheme_level == "central":
                eligible_schemes.append(scheme)
            elif scheme_level == "state" and scheme_state == user_state:
                eligible_schemes.append(scheme)

            if len(eligible_schemes) >= 3:
                break

    return eligible_schemes
