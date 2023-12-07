"""File for validating user input data. Users will input a first_name, a
last_name, and an optional image_url for their Flask Blogly profile. This will
validate the first and last name."""

def validate_names(first_name, last_name):
    """Takes user input of strings first_name and last_name. Checks whether each
    are non-empty strings with non-whitespace characters. If both are valid,
    returns list of stripped first_name and last_name strings.
    Otherwise, returns False."""

    stripped_first_name = first_name.strip()
    stripped_last_name = last_name.strip()

    if len(stripped_first_name) == 0 or len(stripped_last_name) == 0:
        return False
    else:
        return [stripped_first_name, stripped_last_name]






