import re
from exceptions.custom_exceptions import ConstraintError

def validate_regex(value, rules, path):
    if "regex" in rules:
        if not isinstance(value, str) or not re.match(rules["regex"], value):
            raise ConstraintError(f"{path} не відповідає формату")