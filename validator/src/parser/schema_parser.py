from model.schema import Schema, Field

class SchemaParser:
    def parse(self, text):
        schemas = {}
        lines = text.splitlines()

        current_schema = None

        for line in lines:
            line = line.strip()

            if line.startswith("type"):
                name = line.split()[1]
                current_schema = Schema(name)
                schemas[name] = current_schema

            elif ":" in line:
                field_name, field_type = line.split(":")
                field = Field(field_name.strip(), field_type.strip())
                current_schema.add_field(field)

        return schemas