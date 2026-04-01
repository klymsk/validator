from parser.schema_parser import SchemaParser
from parser.data_parser import DataParser
from validator.validator import Validator

def main():
    with open("../../schema.def") as f:
        schema_text = f.read()

    with open("../../data.txt") as f:
        data_text = f.read()

    schema = SchemaParser().parse(schema_text)
    data = DataParser().parse(data_text)

    root_type = list(schema.keys())[0]

    validator = Validator(schema["User"])

    validator.validate(data)

    print("Валідація проейдена!")

if __name__ == "__main__":
    main()