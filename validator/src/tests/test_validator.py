import pytest
from exceptions.custom_exceptions import ConstraintError, MissingFieldError, TypeMismatchError
from validator.validator import Validator
from exceptions.custom_exceptions import *


schema = {
    "name": {"type": str},
    "age": {"type": int, "min": 0, "max": 120}
}


def test_valid_data():
    validator = Validator(schema)
    data = {"name": "Alex", "age": 25}

    assert validator.validate(data) is True


def test_missing_field():
    validator = Validator(schema)
    data = {"name": "Alex"}

    with pytest.raises(MissingFieldError):
        validator.validate(data)


def test_wrong_type():
    validator = Validator(schema)
    data = {"name": "Alex", "age": "25"}

    with pytest.raises(TypeMismatchError):
        validator.validate(data)


def test_constraint_error():
    validator = Validator(schema)
    data = {"name": "Alex", "age": 200}

    with pytest.raises(ConstraintError):
        validator.validate(data)