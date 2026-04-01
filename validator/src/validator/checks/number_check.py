from exceptions.custom_exceptions import ConstraintError

def validate_number(value, rules, path):
    if not isinstance(value, (int, float)):
        return

    if "min" in rules and value < rules["min"]:
        raise ConstraintError(f"{path} менше мінімального значення")

    if "max" in rules and value > rules["max"]:
        raise ConstraintError(f"{path} більше максимального значення")