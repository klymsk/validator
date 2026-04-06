import pytest
from exceptions.custom_exceptions import (
    ConstraintError,
    MissingFieldError,
    TypeMismatchError,
    ValidationError
)
from validator.validator import Validator


# Базові тести
class TestValidatorBasic:
    @pytest.fixture
    def simple_schema(self):
        return {
            "name": {"type": str},
            "age": {"type": int}
        }

    # Перевірка коректних даних
    def test_valid_data(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John", "age": 25}

        assert validator.validate(data) is True

    # Наявність поля
    def test_missing_field(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John"}  # age

        with pytest.raises(MissingFieldError) as exc_info:
            validator.validate(data)

        assert "age" in str(exc_info.value)

    # Перевірка типу
    def test_wrong_type_string(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John", "age": "25"} 

        with pytest.raises(TypeMismatchError):
            validator.validate(data)

    def test_wrong_type_number(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": 123, "age": 25}  # name має бути str, не int

        with pytest.raises(TypeMismatchError):
            validator.validate(data)

# Діапазони
class TestNumberConstraints:
    @pytest.fixture
    def number_schema(self):
        return {
            "id": {"type": int, "min": 1, "max": 9999}
        }

    def test_valid_number(self, number_schema):
        validator = Validator(number_schema)
        assert validator.validate({"id": 100}) is True
        assert validator.validate({"id": 1}) is True
        assert validator.validate({"id": 9999}) is True

    def test_number_below_min(self, number_schema):
        validator = Validator(number_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"id": 0})

        assert "менше" in str(exc_info.value).lower()

    def test_number_above_max(self, number_schema):
        validator = Validator(number_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"id": 10000})

        assert "більше" in str(exc_info.value).lower()

# Тести рядків
class TestStringConstraints:

    @pytest.fixture
    def string_schema(self):
        return {
            "username": {"type": str, "min_length": 3, "max_length": 20}
        }

    def test_valid_string(self, string_schema):
        validator = Validator(string_schema)
        assert validator.validate({"username": "abc"}) is True
        assert validator.validate({"username": "john123"}) is True
        assert validator.validate({"username": "a" * 20}) is True

    def test_string_too_short(self, string_schema):
        validator = Validator(string_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"username": "ab"})

        assert "коротке" in str(exc_info.value).lower()

    def test_string_too_long(self, string_schema):
        validator = Validator(string_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"username": "a" * 21})

        assert "довге" in str(exc_info.value).lower()


# Регулярні вирази
class TestRegexValidation:

    @pytest.fixture
    def email_schema(self):
        return {
            "email": {"type": str, "regex": r".*@.*"}
        }

    # Коректний емайл
    def test_valid_email(self, email_schema):
        validator = Validator(email_schema)
        assert validator.validate({"email": "user@example.com"}) is True
        assert validator.validate({"email": "test@mail.co.uk"}) is True

    def test_invalid_email(self, email_schema):
        validator = Validator(email_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"email": "invalidemail"})

        assert "формату" in str(exc_info.value).lower()

# Вкладені обʼєкти
class TestNestedObjects:

    @pytest.fixture
    def nested_schema(self):
        return {
            "user": {
                "type": dict,
                "schema": {
                    "name": {"type": str},
                    "age": {"type": int}
                }
            }
        }

    # Коректний варіант
    def test_valid_nested_object(self, nested_schema):
        validator = Validator(nested_schema)
        data = {
            "user": {
                "name": "John",
                "age": 25
            }
        }
        assert validator.validate(data) is True

    def test_missing_nested_field(self, nested_schema):
        validator = Validator(nested_schema)
        data = {
            "user": {
                "name": "John"
                # 'age'
            }
        }

        with pytest.raises(MissingFieldError) as exc_info:
            validator.validate(data)

        # Повинно зберігати шлях user.age
        assert "user" in str(exc_info.value)
        assert "age" in str(exc_info.value)

    def test_wrong_type_in_nested(self, nested_schema):
        validator = Validator(nested_schema)
        data = {
            "user": {
                "name": "John",
                "age": "25"  # Має бути int
            }
        }

        with pytest.raises(TypeMismatchError) as exc_info:
            validator.validate(data)

        assert "user.age" in str(exc_info.value)

# Інші типи перевірок
class TestEdgeCases:

    # Пуста схема
    def test_empty_schema(self):
        validator = Validator({})
        assert validator.validate({}) is True

    # Пустий рядок
    def test_empty_string(self):
        schema = {"text": {"type": str, "min_length": 0, "max_length": 10}}
        validator = Validator(schema)
        assert validator.validate({"text": ""}) is True

    def test_zero_value(self):
        schema = {"count": {"type": int, "min": 0, "max": 100}}
        validator = Validator(schema)
        assert validator.validate({"count": 0}) is True

    # Відʼємні числа
    def test_negative_numbers(self):
        schema = {"temperature": {"type": int, "min": -50, "max": 50}}
        validator = Validator(schema)
        assert validator.validate({"temperature": -30}) is True

        with pytest.raises(ConstraintError):
            validator.validate({"temperature": -60})

    # Дробові числа
    def test_float_values(self):
        schema = {"price": {"type": float, "min": 0.0, "max": 1000.0}}
        validator = Validator(schema)
        assert validator.validate({"price": 99.99}) is True

        with pytest.raises(ConstraintError):
            validator.validate({"price": 1000.01})