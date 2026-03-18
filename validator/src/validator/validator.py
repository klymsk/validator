from model.validation_result import ValidationResult


class Validator:
    def validate(self, schema, data_node):
        result = ValidationResult()

        for field in data_node.fields:
            if field not in schema.fields:
                result.add_error(f"{field} not in schema")

        return result