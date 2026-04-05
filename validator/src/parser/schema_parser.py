import re
from exceptions.custom_exceptions import SchemaError

TYPE_MAP = {
    "integer": int,
    "string": str,
    "boolean": bool
}

class SchemaParser:
    def parse(self, text: str):
        try:
            types = {}
            current_type = None

            lines = [line.strip() for line in text.splitlines() if line.strip()]

            for line_num, line in enumerate(lines, 1):
                try:
                    if line.startswith("type"):
                        type_name = line.split()[1]
                        types[type_name] = {}
                        current_type = type_name
                        continue

                    if line == "}":
                        current_type = None
                        continue

                    if current_type:
                        if ":" not in line:
                            raise SchemaError(f"Невірна синтаксис поля на лінії {line_num}: {line}")

                        field, rest = line.split(":", 1)
                        field = field.strip()
                        rest = rest.strip()

                        types[current_type][field] = self._parse_field(rest)
                except SchemaError:
                    raise
                except Exception as e:
                    raise SchemaError(f"Помилка парсингу на лінії {line_num}: {str(e)}")

            # Розв'язуємо вкладені типи (Address, list[User])
            for type_name, fields in types.items():
                for field_name, rules in fields.items():
                    self._resolve_types(rules, types)

            return types
        except SchemaError:
            raise
        except Exception as e:
            raise SchemaError(f"Помилка парсингу схеми: {str(e)}")

    def _parse_field(self, text):
        rules = {}

        # ліст
        list_match = re.match(r"list\[(\w+)\]", text)
        if list_match:
            rules["type"] = list
            rules["items_type"] = list_match.group(1)
            return rules

        # Базові типи
        for key in TYPE_MAP:
            if text.startswith(key):
                rules["type"] = TYPE_MAP[key]

        # Кастомний тип 
        if "type" not in rules:
            rules["type"] = "custom"
            rules["custom_type"] = text.split()[0]

        range_match = re.search(r"range\((\d+),\s*(\d+)\)", text)
        if range_match:
            rules["min"] = int(range_match.group(1))
            rules["max"] = int(range_match.group(2))

        # Довжина
        length_match = re.search(r"length\((\d+),\s*(\d+)\)", text)
        if length_match:
            rules["min_length"] = int(length_match.group(1))
            rules["max_length"] = int(length_match.group(2))

        # Регулярні вирази
        regex_match = re.search(r'regex\("(.+)"\)', text)
        if regex_match:
            rules["regex"] = regex_match.group(1)

        return rules

    def _resolve_types(self, rules, types):
        # ліст
        if rules.get("type") == list and "items_type" in rules:
            type_name = rules["items_type"]
            if type_name in types:
                rules["items"] = types[type_name]
            del rules["items_type"]

        if rules.get("type") == "custom":
            type_name = rules["custom_type"]
            if type_name in types:
                rules["type"] = dict
                rules["schema"] = types[type_name]
            del rules["custom_type"]