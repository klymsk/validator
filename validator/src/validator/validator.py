from exceptions.custom_exceptions import MissingFieldError
from .checks.number_check import validate_number
from .checks.string_check import validate_string
from .checks.regex_check import validate_regex
from .checks.type_check import validate_type

class Validator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, schema = None, path = ""):
        if schema is None:
            schema = self.schema

        for field, rules in schema.items():
            full_path = f"{path}.{field}" if path else field

            if field not in data:
                raise MissingFieldError(f"Поле '{full_path}' відсутнє")
            
            value = data[field]
            expected_type = rules.get("type")

            validate_type(value, expected_type, full_path)

            if expected_type == dict and "schema" in rules:
                self.validate(value, rules["schema"], full_path)
            
            validate_number(value, rules, full_path)
            validate_string(value, rules, full_path)
            validate_regex(value, rules, full_path)

        return True