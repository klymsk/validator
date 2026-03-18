from parser.schema_parser import SchemaParser
from parser.data_parser import DataParser
from validator.validator import Validator
from report.report import ReportGenerator

import sys
import os

sys.path.append(os.path.dirname(__file__))

def main():
    with open("../../schema.def") as f:
        schema_text = f.read()

    with open("../../data.txt") as f:
        data_text = f.read()

    schemas = SchemaParser().parse(schema_text)
    data = DataParser().parse(data_text)

    schema = schemas[data.type_name]

    result = Validator().validate(schema, data)

    ReportGenerator().generate(result)


if __name__ == "__main__":
    main()