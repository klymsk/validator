from exceptions.custom_exceptions import TypeMismatchError

def validate_type(value, expected_type, path):
    if expected_type and not isinstance(value, expected_type):
        raise TypeMismatchError(
            f"Поле '{path}' має бути {expected_type.__name__}, а не {type(value).__name__}"
        )