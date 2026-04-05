import re
from exceptions.custom_exceptions import (
    MissingFieldError,
    ValidationError,
    TypeMismatchError,
    ConstraintError
)

class Validator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, schema=None, path=""):
        try:
            if schema is None:
                schema = self.schema

            for field, rules in schema.items():
                full_path = f"{path}.{field}" if path else field

                if field not in data:
                    raise MissingFieldError(f"Поле '{full_path}' відсутнє")

                value = data[field]
                expected_type = rules.get("type")

                self._validate_type(value, expected_type, full_path)

                if expected_type == dict and "schema" in rules:
                    self.validate(value, rules["schema"], full_path)

                self._validate_number(value, rules, full_path)
                self._validate_string(value, rules, full_path)
                self._validate_regex(value, rules, full_path)

            return True
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Помилка валідації: {str(e)}")

    def _validate_type(self, value, expected_type, path):
        try:
            if expected_type and not isinstance(value, expected_type):
                raise TypeMismatchError(
                    f"Поле '{path}' має бути {expected_type.__name__}, а не {type(value).__name__}"
                )
        except TypeMismatchError:
            raise
        except Exception as e:
            raise TypeMismatchError(f"Помилка перевірки типу для '{path}': {str(e)}")

    def _validate_number(self, value, rules, path):
        try:
            if not isinstance(value, (int, float)):
                return

            if "min" in rules and value < rules["min"]:
                raise ConstraintError(f"{path} менше мінімального значення")

            if "max" in rules and value > rules["max"]:
                raise ConstraintError(f"{path} більше максимального значення")
        except ConstraintError:
            raise
        except Exception as e:
            raise ConstraintError(f"Помилка перевірки числового значення для '{path}': {str(e)}")

    def _validate_string(self, value, rules, path):
        try:
            if not isinstance(value, str):
                return

            if "min_length" in rules and len(value) < rules["min_length"]:
                raise ConstraintError(f"{path} занадто коротке")

            if "max_length" in rules and len(value) > rules["max_length"]:
                raise ConstraintError(f"{path} занадто довге")
        except ConstraintError:
            raise
        except Exception as e:
            raise ConstraintError(f"Помилка перевірки рядка для '{path}': {str(e)}")

    def _validate_regex(self, value, rules, path):
        if "regex" in rules:
            try:
                if not isinstance(value, str) or not re.match(rules["regex"], value):
                    raise ConstraintError(f"{path} не відповідає формату")
            except ConstraintError:
                raise
            except Exception as e:
                raise ConstraintError(f"Помилка перевірки регулярного виразу для '{path}': {str(e)}")