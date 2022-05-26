import re


def is_email_valid(email) -> bool:
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return True if re.search(regex, email) else False
