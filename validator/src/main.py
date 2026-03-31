from parser.data_parser import DataParser
from validator.validator import Validator
from exceptions.custom_exceptions import AppError

def main():
    schema = {
        "name": {
            "type": str,
            "min_length": 2,
            "max_length": 50
        },
        "age": {
            "type": int,
            "min": 0,
            "max": 120
        },
        "address": {
            "type": dict,
            "schema": {
                "city": {"type": str},
                "zip": {"type": int}
            }
        }
    }

    parser = DataParser("data.json")
    
    try:
        data = parser.parse()

        validator = Validator(schema)
        validator.validate(data)

        print("Валідація пройшла успішно!")

    except AppError as e:
        print(f"Помилка валідації: {e}")


if __name__ == "__main__":
    main()