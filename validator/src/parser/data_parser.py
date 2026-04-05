import json
from exceptions.custom_exceptions import ParserError

class DataParser:
    def parse(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ParserError(f"Невірний формат JSON: {str(e)}")
