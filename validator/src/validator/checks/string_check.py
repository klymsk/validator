from exceptions.custom_exceptions import ConstraintError

def validate_string(value, rules, path):
    if not isinstance(value, str):
        return

    if "min_length" in rules and len(value) < rules["min_length"]:
        raise ConstraintError(f"{path} занадто коротке")

    if "max_length" in rules and len(value) > rules["max_length"]:
        raise ConstraintError(f"{path} занадто довге")