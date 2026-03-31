import re
from exceptions.custom_exceptions import (
    MissingFieldError,
    TypeMismatchError,
    ConstraintError
)

class Validator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, schema=None, path=""):
        if schema is None:
            schema = self.schema

        for field, rules in schema.items():
            full_path = f"{path}.{field}" if path else field

            # Перевірка полів
            if field not in data:
                raise MissingFieldError(f"Поле '{full_path}' відсутнє")

            # Перевірка типу
            value = data[field]
            expected_type = rules.get("type")
            if expected_type and not isinstance(value, expected_type):
                raise TypeMismatchError(
                    f"Поле '{full_path}' має бути {expected_type.__name__}, а не {type(value).__name__}"
                )

            # Вкладена структура
            if expected_type == dict and "schema" in rules:
                self.validate(value, rules["schema"], full_path)

            # Числа
            if isinstance(value, (int, float)):
                if "min" in rules and value < rules["min"]:
                    raise ConstraintError(f"{full_path} менше мінімального значення")

                if "max" in rules and value > rules["max"]:
                    raise ConstraintError(f"{full_path} більше максимального значення")

            # Довжина рядка
            if isinstance(value, str):
                if "min_length" in rules and len(value) < rules["min_length"]:
                    raise ConstraintError(f"{full_path} занадто коротке")

                if "max_length" in rules and len(value) > rules["max_length"]:
                    raise ConstraintError(f"{full_path} занадто довге")
                
            if expected_type == list:
                if not isinstance(value, list):
                    raise TypeMismatchError(f"{full_path} має бути списком")

                # якщо є схема елементів
                if "items" in rules:
                    for i, item in enumerate(value):
                        self.validate(
                            {f"item_{i}": item},
                            {f"item_{i}": rules["items"]},
                            full_path
                        )

            # REGEX
            if "regex" in rules:
                if not re.match(rules["regex"], value):
                    raise ConstraintError(f"{full_path} не відповідає формату")

        return True